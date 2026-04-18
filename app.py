import streamlit as st
from pypdf import PdfReader
import io
from datetime import datetime

st.set_page_config(page_title='AI CS Assistant Production', layout='wide')

ss = st.session_state
for k, v in {
    'history': [],
    'progress': {'topics': 0, 'quizzes': 0},
    'docs': '',
    'files': []
}.items():
    if k not in ss:
        ss[k] = v

# ---------- HELPERS ----------
def read_pdfs(files):
    text = ''
    meta = []
    for f in files:
        try:
            reader = PdfReader(io.BytesIO(f.read()))
            pages = len(reader.pages)
            content = ''
            for p in reader.pages:
                content += (p.extract_text() or '') + "\n"
            text += content + "\n"
            meta.append((f.name, pages, 'PDF'))
        except Exception:
            meta.append((f.name, 0, 'Failed'))
    return text, meta

def retrieve(q):
    if not ss.docs:
        return 'No study material processed yet.'
    lines = ss.docs.split("\n")
    hits = [x for x in lines if any(w.lower() in x.lower() for w in q.split())]
    return "\n".join(hits[:10]) or ss.docs[:1500]

def save_history(tag):
    ss.history.append(f"{datetime.now().strftime('%H:%M')} | {tag}")

# ---------- HEADER ----------
st.title('🎓 AI CS Assistant Production')
st.caption('Professional academic learning platform for Computer Science students')

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header('📂 Multi-Document Upload')
    files = st.file_uploader('Upload Materials', type=['pdf'], accept_multiple_files=True)

    if st.button('Process Files'):
        if files:
            ss.docs, ss.files = read_pdfs(files)
            st.success('Files processed successfully!')
        else:
            st.error('Please upload at least one PDF.')

    page = st.radio('Navigate', ['Dashboard', 'Ask & Solve', 'Browser', 'Export', 'Progress', 'History', 'README'])

# ---------- PAGES ----------
if page == 'Dashboard':
    st.subheader('📊 Subject Dashboard')
    c1, c2, c3 = st.columns(3)
    c1.metric('Files Loaded', len(ss.files))
    c2.metric('Topics Studied', ss.progress['topics'])
    c3.metric('Quizzes Taken', ss.progress['quizzes'])

    if ss.files:
        st.write('### Uploaded Materials')
        for f in ss.files:
            st.write(f'- {f[0]} | {f[1]} pages | {f[2]}')

elif page == 'Ask & Solve':
    st.subheader('💬 Topic Explanations + Question Solving')
    mode = st.selectbox('Mode', ['Explain Topic', 'Solve Question', 'Generate MCQ'])
    q = st.text_area('Enter your query')

    if st.button('Run'):
        if not q.strip():
            st.warning('Enter a valid academic query.')
        else:
            result = retrieve(q)
            st.write(result)
            save_history(mode + ': ' + q[:40])
            ss.progress['topics'] += 1
            if mode == 'Generate MCQ':
                ss.progress['quizzes'] += 1

elif page == 'Browser':
    st.subheader('📚 Content Browser')
    key = st.text_input('Search topic / keyword')

    if st.button('Search'):
        st.write(retrieve(key))
        st.info('Related materials shown using keyword matching.')

elif page == 'Export':
    st.subheader('📤 Export Study Guide')
    txt = st.text_area('Enter notes to export')
    st.download_button('Download TXT', txt, file_name='study_guide.txt')

elif page == 'Progress':
    st.subheader('📈 Learning Progress')
    st.metric('Topics Studied', ss.progress['topics'])
    st.metric('Quizzes Taken', ss.progress['quizzes'])

elif page == 'History':
    st.subheader('🕘 Activity History')
    if ss.history:
        for h in reversed(ss.history[-30:]):
            st.write('- ' + h)
    else:
        st.info('No activity yet.')

else:
    st.subheader('📘 README / Usage Guide')
    st.markdown("""
### Setup
1. Install requirements.txt
2. Run: py -m streamlit run app.py
3. Upload PDFs
4. Use Ask & Solve page

### Features
- Multi-document upload
- Topic explanation
- Question solving
- MCQ generation
- Content browser
- Export notes
- Progress tracking
- History

### Demo Video Idea (5-7 min)
- Show upload
- Ask topic question
- Solve exam question
- Generate MCQ
- Export notes
- Show dashboard
""")
