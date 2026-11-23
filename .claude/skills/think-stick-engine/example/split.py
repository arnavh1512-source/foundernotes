"""Version 2 voices: characters speak their own lines; the narrator only tells the story.
Writes v2/narration/script.json (narrator), v2/dialogue/script.json (ElevenLabs), v2/order.json and v2/groups.json
(groups map each original segment id -> new ids, so the existing shot list keeps its timing)."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
old_n = {s['id']: s for s in json.load(open('../narration/script.json'))['segments']}
old_d = {s['id']: s for s in json.load(open('../dialogue/script.json'))['segments']}
old_order = json.load(open('../order.json'))
N, Y, P, M = 'N', 'youth', 'philosopher', 'mother'
NEW = {
 'n02': [(N, "You would say the anger made you do it. It just came out. Now picture a mother yelling at her daughter."),
         (M, "How many times do I have to tell you? Clean up this mess, right now!"),
         (N, "The phone rings. She picks it up."),
         (M, "Hello? Oh, good afternoon! Yes, of course. Thank you so much for calling."),
         (N, "Her voice is suddenly calm and polite. It is the teacher.")],
 'n06': [(N, "This is the young man's counterattack. Last time the philosopher said we act toward goals, not from causes."),
         (Y, "Fine. Then explain this. I'm not someone who shouts in public. The anger came out of nowhere. Where is the goal in that?")],
 'n07': [(N, "But the philosopher's point is serious."),
         (P, "If anger can be blamed for anything we do, then nobody is responsible for anything they do while angry. So here is another explanation. You didn't get angry and then start shouting. You wanted the waiter to give in and listen to you, and shouting was the quickest way. So you created the anger to do the job.")],
 'n08': [(P, "I call it fabricating anger. Not faking it. The anger is real. But it was made for a purpose."),
         (N, "And think about what else you could have done. Explain calmly, and the waiter would almost certainly have apologised, wiped your jacket, and offered to pay for the dry cleaning. Shouting just felt faster.")],
 'n09': [(N, "That is when the philosopher tells the story of the mother and the phone."),
         (P, "Her anger was strong enough to fill the room, and it vanished in a single word, hello, because her goal changed. It came straight back the moment the call ended, because the goal came back. Anger is a tool for pushing people and winning arguments. It can be taken out and put away as needed.")],
 'n11': [(N, "It is a strong objection. We are moved by grief, love, fear and joy."),
         (Y, "If all of that is just equipment for getting what we want, then people are machines, and life is cold. That's nihilism!")],
 'n12': [(N, "And here the philosopher turns the argument around."),
         (P, "The real machine is the other view: the idea that a cause in your past produces a result in your present, as automatically as one gear turns another. If that were true, nobody could do anything differently. It is that view, not mine, that treats people like machines and denies their free will.")],
 'n14': [(N, "Before he can, the philosopher gives an image."),
         (P, "Imagine a well where the water is always eighteen degrees, all year round. In winter, it feels warm. In summer, it feels cold. The water never changed. Only the way you met it.")],
 'n15': [(P, "A divorce in someone's childhood is like that water. It happened. It is a fact. But does it feel cold, or warm? That is decided now, by the meaning you give it."),
         (N, "And the young man, almost against his will, puts it in one line.")],
 'n16': [(P, "If we believe the past decides everything, we are stuck in a story with no way forward, and that leads to pessimism and giving up on life. Believe that people can change, and you have to look forward, at goals, as a matter of course.")],
 'n18': [(N, "He has a friend called Y. Bright, easy, the kind of person everyone smiles at when he walks in. Like a sunflower. And the young man is the opposite: awkward, and sure he could never be like that. So he sets a trap."),
         (Y, "You say anyone can change. Could I become someone like Y?")],
 'n19': [(P, "No. You just don't understand it yet. And the first step to change is knowing."),
         (N, "But he will not hand over answers either. He points out that Socrates never wrote a single book; he argued with people in public. Adler talked with people in cafes in Vienna."),
         (P, "Answers from others are stopgaps. The ones you argue your way to are the ones that change you."),
         (N, "So they agree to keep going, until one of them gives in.")],
 'n20': [(N, "Then comes a line for anyone who loves self help. The young man reads book after book."),
         (P, "No amount of knowledge will change you if the base stays the same. It just piles up, and sooner or later it is thrown away."),
         (N, "Reading about change is not changing.")],
 'n21': [(N, "So why does he want to be Y? The philosopher's guess is gentle and sharp at once."),
         (P, "Right now you cannot feel really happy, because you have not learned to love yourself. So you dream of being reborn as somebody else.")],
 'n22': [(N, "The philosopher does not flinch."),
         (P, "Ask around, and you would struggle to find anyone who says, yes, I like myself, and means it."),
         (Y, "Do you like yourself?"),
         (P, "At the very least, I don't want to be a different person. I accept who I am.")],
 'n23': [(N, "But he is careful."),
         (P, "I am not saying it is fine to stay just as you are. If you are unhappy, you cannot stop there. You have to put one foot in front of the other."),
         (N, "And he quotes Adler.")],
 'n25': [(N, "The philosopher does not deny any of it."),
         (P, "Unfairness is real. But fixating on what you were born with will not change it. We are not replaceable machines. What we need is not replacement. It is renewal."),
         (N, "And then he says the thing that makes the young man's face burn.")],
 'n26': [(N, "He borrows an old Greek idea, sometimes called the Socratic paradox."),
         (P, "Nobody desires what is bad for them. Even criminals have a reason that, to them, makes the crime seem worth it."),
         (N, "And in ancient Greek, the word for good did not mean morally good. It meant beneficial. The word for bad meant not beneficial.")],
 'n27': [(P, "So when I say you chose unhappiness because it was good for you, I mean it did something for you. It protected you from something."),
         (Y, "Protected me from what, exactly?"),
         (P, "That will become clearer as we argue."),
         (N, "The young man stands up and glares. He is being made a fool of, he decides. He will make this man kneel before him, whatever it takes.")],
 'n29': [(P, "First, a word. Adler did not talk about personality. He talked about lifestyle. Not clothes and hobbies: your tendencies of thought and action. How you see the world, and how you see yourself.")],
 'n30': [(N, "Here is a small trick from the book."),
         (P, "Take a person who says, I am a pessimist. Rephrase it: I have a pessimistic view of the world."),
         (N, "Personality sounds fixed, like eye colour. A view of the world is something you can look at, question and change.")],
 'n31': [(N, "And here is the controversial part."),
         (P, "Adler thought we choose our lifestyle, usually around the age of ten. Not consciously, and not alone: race, culture, family and the home we grew up in all push hard. But in the end, it was you who settled on this kind of self. And what was chosen can be chosen again.")],
 'n32': [(P, "You can. People can change at any time, in any environment. You are unable to change because you keep making the decision not to."),
         (N, "The young man is outraged. He sincerely wants to change. How could he be deciding not to?")],
 'n33': [(N, "Here is the image."),
         (P, "A lifestyle is like driving an old, familiar car. It rattles a bit and pulls to one side, but you know exactly how it handles. A new car might be better, but you cannot predict it. You don't know what will happen, and that is frightening. So people complain about the old car, and keep driving it.")],
 'n34': [(P, "When we try to change, we have two options: the anxiety of changing, or the disappointment of not changing. Most of us pick the disappointment, because at least it is familiar."),
         (N, "That is what he means by unhappiness you chose."),
         (P, "It is not that you lack ability. You lack the courage to be happy.")],
 'n35': [(N, "So what should you actually do?"),
         (P, "The first step is to stop using one sentence. If only. If only I had more time. If only I were like Y. As long as you live in the world of if only, you never have to find out.")],
 'n36': [(P, "There is a young man who dreams of becoming a novelist, and never finishes anything. His job keeps him too busy, he says. One day, when he has the time, he will write the book that wins the prize.")],
 'n37': [(P, "But as long as the book is unfinished, it can still be brilliant. Finishing it means sending it out, being judged, maybe being rejected. So the busy job is not the reason. It is the protection. And in five or ten years the excuse just changes shape. I am not young any more. I have a family to think about.")],
 'n38': [(P, "Look at how much of life works like this. Simple tasks we keep finding reasons not to do. The thing making it complicated is not the world. It is the self.")],
 'n39': [(N, "But look at what the medicine gives back. If your past decided everything, you could do nothing. If your choices decide it, you can choose again."),
         (P, "Change your lifestyle, the way you give meaning to the world and yourself, and your behaviour has to change with it. It might seem hard, but it is really quite simple.")],
 'n40': [(P, "No. You are not being blamed. No matter what has happened up to now, it need not decide how you live from now on. You, living here and now, are the one who decides."),
         (N, "It is a hard line, and last time we saw where Adler pushes it too far. Some experiences need real help, and if your past is weighing on you, talking to a professional is a strong step. But the useful part survives: your life is decided here and now.")],
 'n43': [(N, "At the end of the night, the young man is not convinced."),
         (Y, "I disagree with a hundred per cent of what you've said. My head feels like it might burst. I'm sorry I was rude. Can I come back?"),
         (N, "The philosopher just smiles."),
         (P, "Come whenever you like."),
         (N, "That is what a dialogue is supposed to be like.")],
}
VOICES = {'youth': 'TX3LPaxmHKxFdv7VOQHJ', 'philosopher': 'pqHfZKP75CvOlQylNhV4', 'mother': 'XrExE9yKIg1WjnnlVkGX'}
nar, dia, order, groups = [], [], [], {}
for gid in old_order:
    if gid in old_d:                                   # unchanged character line
        s = old_d[gid]; dia.append({k: s[k] for k in ('id', 'speaker', 'text', 'pause_after')} | {'scene_id': gid})
        order.append(gid); groups[gid] = [gid]; continue
    parts = NEW.get(gid)
    if not parts:                                      # unchanged narrator segment keeps its id (cached take reused)
        nar.append(old_n[gid]); order.append(gid); groups[gid] = [gid]; continue
    ids = []
    for i, (who, text) in enumerate(parts):
        sid = f"{gid}{'abcdefg'[i]}" if who == N else f"{gid}{'abcdefg'[i]}_{who[0]}"
        last = i == len(parts) - 1
        pause = old_n[gid].get('pause_after', .5) if last else (.35 if who == N else .4)
        if who == N: nar.append({'id': sid, 'section': old_n[gid].get('section', ''), 'text': text, 'pause_after': pause})
        else: dia.append({'id': sid, 'speaker': who, 'scene_id': gid, 'text': text, 'pause_after': pause})
        ids.append(sid); order.append(sid)
    groups[gid] = ids
os.makedirs('narration', exist_ok=True); os.makedirs('dialogue', exist_ok=True)
json.dump({**{k: v for k, v in json.load(open('../narration/script.json')).items() if k != 'segments'}, 'segments': nar}, open('narration/script.json', 'w'), indent=1)
json.dump({'project': 'Night 1 part 2 v2: characters speak their own lines', 'speakers': {k: {'voice_id': v} for k, v in VOICES.items()},
           'lead': 0.1, 'tail': 0.3, 'segments': dia}, open('dialogue/script.json', 'w'), indent=1)
json.dump(order, open('order.json', 'w')); json.dump(groups, open('groups.json', 'w'), indent=0)
w = lambda L: sum(len(s['text'].split()) for s in L)
print(f"narrator {len(nar)} segs {w(nar)} words | characters {len(dia)} lines {w(dia)} words | total {w(nar)+w(dia)}")
print('new narrator segs to record:', sum(1 for s in nar if s['id'] not in old_n))
print('new character lines:', sum(1 for s in dia if s['id'] not in old_d))
