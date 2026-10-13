import json, random, time, csv, io
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="MindSprint AI Quiz", page_icon="🧠", layout="centered")
st.markdown("""<style>.stApp{background:linear-gradient(135deg,#fff5f8 0%,#f7f1ff 100%)}.block-container{max-width:900px;padding-top:2rem}.hero{padding:1.5rem;border-radius:20px;background:#fff;border:1px solid #f0d9e4}.small-muted{color:#6b6470;font-size:.92rem}</style>""",unsafe_allow_html=True)

@st.cache_data
def load_questions():
    with (Path(__file__).parent/'questions.json').open(encoding='utf-8') as f: return json.load(f)
ALL_QUESTIONS=load_questions()

def reset_quiz():
    for key in list(st.session_state.keys()):
        if key.startswith(('answer_','match_','hint_','show_')): st.session_state.pop(key,None)
    for key in ['quiz_questions','current','score','answers','started_at','player_name']: st.session_state.pop(key,None)

def is_correct(q,response):
    fmt=q.get('format','MCQ')
    if fmt=='Fill in the Blank': return str(response or '').strip().casefold() in [a.casefold() for a in q.get('accepted_answers',[])]
    if fmt=='Match the Following': return isinstance(response,dict) and response=={p['left']:p['right'] for p in q['match_pairs']}
    return isinstance(response,int) and response==q.get('answer')

def answer_text(q,response):
    fmt=q.get('format','MCQ')
    if fmt=='Fill in the Blank': return str(response or '').strip() or '(No answer)'
    if fmt=='Match the Following': return '; '.join(f'{k} → {v}' for k,v in response.items()) if isinstance(response,dict) else '(No answer)'
    return q['options'][response] if isinstance(response,int) else str(response or '(No answer)')

def correct_text(q):
    fmt=q.get('format','MCQ')
    if fmt=='Fill in the Blank': return q.get('answer_display','Sensors')
    if fmt=='Match the Following': return '; '.join(f"{p['left']} → {p['right']}" for p in q['match_pairs'])
    return q['options'][q['answer']]

st.title('🧠 MindSprint AI Quiz')
st.caption('Artificial Intelligence • Units I & II')
with st.sidebar:
    st.header('About this game'); st.write('Practice AI foundations, agents, environments, search strategies, CSPs and Means-End Analysis.')
    st.write(f"**Question bank:** {len(ALL_QUESTIONS)} questions")
    st.divider(); st.write('**Scoring**'); st.write('1 point for each correct answer. Submit an answer to receive feedback.')
    st.write('**Formats:** MCQ, True/False, fill-in-the-blank, matching, assertion–reason, scenario and problem-solving.')
if 'page' not in st.session_state: st.session_state.page='home'

if st.session_state.page=='home':
    st.markdown('<div class="hero"><h2>Think. Search. Solve.</h2><p>Test your understanding of Artificial Intelligence with an interactive quiz.</p><p class="small-muted">Includes concept checks, real-world scenarios, matching, fill-in-the-blank and search problems.</p></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        count_label=st.selectbox('Quiz length',['10 random questions','25 random questions','All 50 questions'])
        difficulty=st.selectbox('Difficulty',['All levels','Easy','Medium','Hard'])
    with c2:
        topics=sorted({q['topic'] for q in ALL_QUESTIONS}); topic=st.selectbox('Topic filter',['All topics']+topics)
        name=st.text_input('Your name (optional)',placeholder='Enter your name')
    st.info('Use the hint button if you get stuck. Try answering before opening a hint.')
    if st.button('🚀 Start Quiz',type='primary',use_container_width=True):
        pool=ALL_QUESTIONS[:]
        if difficulty!='All levels': pool=[q for q in pool if q['difficulty']==difficulty]
        if topic!='All topics': pool=[q for q in pool if q['topic']==topic]
        if not pool: st.error('No questions match those filters. Please change the filters.')
        else:
            random.shuffle(pool); count={'10 random questions':10,'25 random questions':25,'All 50 questions':50}[count_label]
            st.session_state.quiz_questions=pool[:min(count,len(pool))]; st.session_state.current=0; st.session_state.score=0; st.session_state.answers=[]
            st.session_state.started_at=time.time(); st.session_state.player_name=name.strip() or 'Student'; st.session_state.page='quiz'; st.rerun()

elif st.session_state.page=='quiz':
    qs=st.session_state.quiz_questions; idx=st.session_state.current
    if idx>=len(qs): st.session_state.page='results'; st.rerun()
    q=qs[idx]; fmt=q.get('format','MCQ'); st.progress((idx+1)/len(qs),text=f"Question {idx+1} of {len(qs)}")
    st.markdown(f"**Topic:** {q['topic']} · **Format:** {fmt} · **Difficulty:** {q['difficulty']}"); st.subheader(q['question'])
    submitted=next((a for a in st.session_state.answers if a['id']==q['id']),None)
    if submitted is None:
        response=None
        if fmt=='Fill in the Blank': response=st.text_input('Type your answer',key=f"answer_{q['id']}",placeholder='Enter your answer')
        elif fmt=='Match the Following':
            lefts=[p['left'] for p in q['match_pairs']]; rights=[p['right'] for p in q['match_pairs']]
            choice_key=f"match_choices_{q['id']}"
            if choice_key not in st.session_state: st.session_state[choice_key]=random.sample(rights,len(rights))
            response={}
            for left in lefts: response[left]=st.selectbox(f'Match: {left}',st.session_state[choice_key],key=f"match_{q['id']}_{left}")
        else:
            choice=st.radio('Choose one answer:',q['options'],index=None,key=f"answer_{q['id']}")
            response=q['options'].index(choice) if choice is not None else None
        if st.button('💡 Show hint',key=f"show_{q['id']}"): st.session_state[f"hint_{q['id']}"]=True
        if st.session_state.get(f"hint_{q['id']}"): st.info(q.get('hint','Identify what the question asks and compare the choices carefully.'))
        left,right=st.columns(2)
        with left:
            if st.button('Submit answer',type='primary',use_container_width=True):
                if fmt=='Fill in the Blank' and not str(response or '').strip(): st.warning('Type an answer first.'); st.stop()
                if fmt!='Fill in the Blank' and fmt!='Match the Following' and response is None: st.warning('Please select an option first.'); st.stop()
                ok=is_correct(q,response)
                if ok: st.session_state.score+=1
                st.session_state.answers.append({'id':q['id'],'question':q['question'],'selected':response,'is_correct':ok,'explanation':q['explanation'],'topic':q['topic']})
                st.rerun()
        with right:
            if st.button('End quiz',use_container_width=True): st.session_state.page='results'; st.rerun()
    else:
        if submitted['is_correct']:
            st.success('Correct! +1 point')
        else:
            st.error(f"Not quite. Correct answer: {correct_text(q)}")
        st.write(q['explanation'])
        if st.button('Next question',type='primary',use_container_width=True): st.session_state.current+=1; st.rerun()

elif st.session_state.page=='results':
    qs=st.session_state.quiz_questions; answers=st.session_state.answers; score=st.session_state.score; pct=score/len(qs)*100 if qs else 0
    elapsed=int(time.time()-st.session_state.started_at); st.balloons()
    st.markdown('<div class="hero"><h2>Quiz complete 🎉</h2><p>Your results are ready.</p></div>',unsafe_allow_html=True)
    st.write(f"**Student:** {st.session_state.get('player_name','Student')}")
    a,b,c=st.columns(3); a.metric('Score',f'{score}/{len(qs)}'); b.metric('Percentage',f'{pct:.1f}%'); c.metric('Time taken',f'{elapsed//60}m {elapsed%60}s')
    if pct>=80: st.success('Excellent work! You have a strong grasp of these topics.')
    elif pct>=50: st.info('Good effort. Review the explanations for questions you missed.')
    else: st.warning('Keep practising. Revisit the concepts and try another round.')
    st.subheader('Review your answers')
    for n,ans in enumerate(answers,1):
        q=next(item for item in ALL_QUESTIONS if item['id']==ans['id'])
        with st.expander(f"{n}. {'✅' if ans['is_correct'] else '❌'} {ans['question']}"):
            st.write(f"**Your answer:** {answer_text(q,ans['selected'])}"); st.write(f"**Correct answer:** {correct_text(q)}"); st.write(ans['explanation'])
    st.subheader('Topic-wise performance'); topic_scores={}
    for ans in answers:
        item=topic_scores.setdefault(ans['topic'],{'correct':0,'total':0}); item['total']+=1; item['correct']+=int(ans['is_correct'])
    for topic,result in sorted(topic_scores.items()): st.write(f"**{topic}:** {result['correct']}/{result['total']}"); st.progress(result['correct']/result['total'])
    out=io.StringIO(); writer=csv.writer(out); writer.writerow(['Question','Topic','Your answer','Correct answer','Correct','Explanation'])
    for ans in answers:
        q=next(item for item in ALL_QUESTIONS if item['id']==ans['id']); writer.writerow([ans['question'],ans['topic'],answer_text(q,ans['selected']),correct_text(q),ans['is_correct'],ans['explanation']])
    st.download_button('Download results as CSV',out.getvalue().encode('utf-8-sig'),file_name='mindSprint_quiz_results.csv',mime='text/csv',use_container_width=True)
    if st.button('Play again',type='primary',use_container_width=True): reset_quiz(); st.session_state.page='home'; st.rerun()
