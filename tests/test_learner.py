"""Tests of the learning filter, the image hash and a small labeled corpus."""

import io
import random
import unittest

from PIL import Image, ImageDraw

from guardbot import imgsim, learner

SCAM = [
    "Congratulations you won 5000 USDT, claim your free crypto giveaway now at http://claim-usdt.top",
    "MrBeast giveaway! Double your bitcoin, send 0.1 BTC get 0.2 BTC back, limited time http://btc-double.xyz",
    "Free nitro for everyone, click http://discorcl-gift.com to claim your gift before it expires",
    "Elon Musk is giving away ethereum today, connect your wallet to claim http://eth-gift.live",
    "Earn 300 dollars per day with this trading bot, guaranteed profit, message me for the link http://profit-bot.top",
    "Steam gift 50 dollars for you, claim now http://steamcommunlty.ru/gift",
    "You have been selected for a free airdrop, connect wallet here http://airdrop-claim.xyz",
    "Join now and win free crypto, giveaway ends soon http://win-crypto.top",
    "Get free robux and nitro, verify your account here http://free-robux.top",
    "Bitcoin giveaway live now, send crypto and receive double back http://btc-live.xyz",
]
HAM = [
    "Hey, does anyone want to play tonight around 8?", "I think the new patch fixed the lag in the lobby", "Can someone explain how the level system works here?",
    "Thanks for the help yesterday, it works now", "What time is the event on Saturday?", "I will be away for the weekend, see you Monday",
    "Check out the rules channel before posting please", "The movie was great, the ending was a bit slow though", "Anyone know a good recipe for pasta without cream?",
    "My internet is down again, I'll join later", "Happy birthday! Have a great day", "Does this bot support custom commands for roles?",
    "I finished the quest, the boss was really hard", "Let's meet in the voice channel in ten minutes", "Good morning everyone, coffee is ready",
    "Is the server restart tonight or tomorrow?", "I like the new avatar, who made it?", "We need two more people for the raid",
    "How do I change my nickname on this server?", "The music in this game is amazing", "Sorry for the late reply, I was at work",
    "Did you see the match yesterday? What a goal", "I'm learning python, any tips for beginners?", "Please keep the chat clean and friendly",
    "That meme was so good, I laughed for minutes", "Could a moderator help me with my role please?", "Let me know when the stream starts",
    "I forgot my password for the forum, who can help", "The library closes at six so I will study at home", "Welcome to the server, enjoy your stay",
    "Does anybody have the link to the wiki page?", "Training starts at seven, don't be late", "I bought a new keyboard and it feels great",
    "The weather here is terrible today", "We could play chess later if you want",
]


def trained():
    m = learner.new_model()
    for t in SCAM[:8]:
        learner.train(m, t, True)
    for t in HAM[:30]:
        learner.train(m, t, False)
    return m


class LearnerTest(unittest.TestCase):
    def test_not_ready_means_no_opinion(self):
        m = learner.new_model()
        learner.train(m, SCAM[0], True)
        self.assertEqual(learner.probability(m, SCAM[1]), 0.5)

    def test_held_out_examples(self):
        m = trained()
        self.assertTrue(learner.ready(m))
        scams = [learner.probability(m, t) for t in SCAM[8:]]
        hams = [learner.probability(m, t) for t in HAM[30:]]
        self.assertTrue(all(p >= learner.ACT for p in scams), scams)
        self.assertTrue(all(p < learner.ACT for p in hams), hams)  # with so few examples the filter must at least never act on normal talk

    def test_only_hashes_are_stored(self):
        m = trained()
        self.assertTrue(all(len(k) == 10 for k in m["scam"]))
        self.assertNotIn("giveaway", str(m))

    def test_untrain_and_prune(self):
        m = learner.new_model()
        learner.train(m, SCAM[0], True)
        learner.untrain(m, SCAM[0], True)
        self.assertEqual((m["n_scam"], m["scam"]), (0, {}))
        table = {str(i): i for i in range(learner.MAX_FEATURES + 50)}
        learner.prune(table)
        self.assertLess(len(table), learner.MAX_FEATURES)

    def test_tiny_texts_are_ignored(self):
        self.assertFalse(learner.train(learner.new_model(), "ok", True))


def picture(seed, size=(200, 160), jpeg=False, scale=1.0, tweak=False):
    rnd = random.Random(seed)
    im = Image.new("RGB", (200, 160), (240, 240, 240))
    d = ImageDraw.Draw(im)
    for _ in range(14):
        x, y = rnd.randint(0, 150), rnd.randint(0, 110)
        d.rectangle([x, y, x + rnd.randint(10, 60), y + rnd.randint(10, 50)], fill=tuple(rnd.randint(0, 255) for _ in range(3)))
    if tweak:
        d.ellipse([5, 5, 15, 15], fill=(0, 0, 0))
    if scale != 1.0:
        im = im.resize((int(200 * scale), int(160 * scale)))
    buf = io.BytesIO()
    im.save(buf, "JPEG" if jpeg else "PNG", quality=60) if jpeg else im.save(buf, "PNG")
    return buf.getvalue()


class ImageTest(unittest.TestCase):
    def test_same_picture_in_other_forms_is_close(self):
        base = imgsim.dhash(picture(1))
        for variant in (picture(1, jpeg=True), picture(1, scale=0.5), picture(1, tweak=True)):
            self.assertLessEqual(imgsim.distance(base, imgsim.dhash(variant)), imgsim.NEAR)
        self.assertTrue(imgsim.similar(base, [imgsim.dhash(picture(1, jpeg=True))]))

    def test_other_pictures_are_far(self):
        base = imgsim.dhash(picture(1))
        far = [imgsim.distance(base, imgsim.dhash(picture(s))) for s in range(2, 12)]
        self.assertGreater(min(far), imgsim.NEAR)

    def test_flat_pictures_never_match_and_garbage_is_refused(self):
        buf = io.BytesIO()
        Image.new("RGB", (50, 50), (255, 255, 255)).save(buf, "PNG")
        flat = imgsim.dhash(buf.getvalue())
        self.assertFalse(imgsim.similar(flat, [flat]))
        with self.assertRaises(ValueError):
            imgsim.dhash(b"not an image")


if __name__ == "__main__":
    unittest.main()
