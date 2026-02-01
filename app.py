import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="Job Market Analyzer", page_icon="💼", layout="wide")

# Title
st.title("💼 Job Market Intelligence Platform")
st.markdown("Analyze job market trends, discover in-demand skills, and get personalized career recommendations.")

# Skills lists
TECH_SKILLS = [
    'python', 'java', 'javascript', 'sql', 'excel', 'tableau', 'power bi',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'linux',
    'react', 'angular', 'node.js', 'typescript', 'html', 'css',
    'machine learning', 'deep learning', 'data science', 'ai', 'nlp',
    'tensorflow', 'pytorch', 'pandas', 'numpy', 'spark', 'hadoop',
    'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
    'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum',
    'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'scala', 'kotlin', 'swift',
    'salesforce', 'sap', 'oracle', 'jira', 'confluence'
]

SOFT_SKILLS = [
    'communication', 'leadership', 'teamwork', 'problem solving',
    'analytical', 'project management', 'time management', 'organization',
    'collaboration', 'presentation', 'negotiation', 'customer service',
    'critical thinking', 'attention to detail', 'multitasking',
    'interpersonal', 'adaptability', 'creativity', 'initiative'
]

@st.cache_data
def load_data():
    df = pd.read_csv('postings_small.csv')
    return df

@st.cache_data
def extract_skills(df):
    def get_skills(text, skill_list):
        if pd.isna(text):
            return []
        text = str(text).lower()
        return [skill for skill in skill_list if skill.lower() in text]
    
    df['tech_skills'] = df['description'].apply(lambda x: get_skills(x, TECH_SKILLS))
    df['soft_skills'] = df['description'].apply(lambda x: get_skills(x, SOFT_SKILLS))
    return df

# Load data
with st.spinner("Loading job data..."):
    df = load_data()
    df = extract_skills(df)

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select Page", [
    "Overview",
    "Skills Analysis", 
    "Salary Insights",
    "Job Recommendations",
    "Skills Gap Analysis"
])

# ============ OVERVIEW PAGE ============
if page == "Overview":
    st.header("Market Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs", f"{len(df):,}")
    col2.metric("Companies", f"{df['company_name'].nunique():,}")
    col3.metric("Unique Titles", f"{df['title'].nunique():,}")
    
    salary_df = df[df['max_salary'].notna() & (df['max_salary'] > 0) & (df['max_salary'] < 500000)]
    col4.metric("Avg Salary", f"${salary_df['max_salary'].mean():,.0f}")
    
    st.markdown("---")
    
    # Top job titles
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Job Titles")
        top_titles = df['title'].value_counts().head(10)
        fig = px.bar(x=top_titles.values, y=top_titles.index, orientation='h',
                     labels={'x': 'Count', 'y': 'Job Title'})
        fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Companies Hiring")
        top_companies = df['company_name'].value_counts().head(10)
        fig = px.bar(x=top_companies.values, y=top_companies.index, orientation='h',
                     labels={'x': 'Count', 'y': 'Company'}, color=top_companies.values)
        fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Experience level distribution
    st.subheader("Jobs by Experience Level")
    exp_counts = df['formatted_experience_level'].value_counts()
    fig = px.pie(values=exp_counts.values, names=exp_counts.index, 
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ============ SKILLS ANALYSIS PAGE ============
elif page == "Skills Analysis":
    st.header("Skills in Demand")
    
    # Count skills
    all_tech = []
    for skills in df['tech_skills']:
        all_tech.extend(skills)
    tech_counts = Counter(all_tech)
    
    all_soft = []
    for skills in df['soft_skills']:
        all_soft.extend(skills)
    soft_counts = Counter(all_soft)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 15 Tech Skills")
        top_tech = tech_counts.most_common(15)
        fig = px.bar(x=[x[1] for x in top_tech], y=[x[0] for x in top_tech],
                     orientation='h', color=[x[1] for x in top_tech],
                     color_continuous_scale='blues')
        fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 15 Soft Skills")
        top_soft = soft_counts.most_common(15)
        fig = px.bar(x=[x[1] for x in top_soft], y=[x[0] for x in top_soft],
                     orientation='h', color=[x[1] for x in top_soft],
                     color_continuous_scale='greens')
        fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ============ SALARY INSIGHTS PAGE ============
elif page == "Salary Insights":
    st.header("Salary Insights")
    
    salary_df = df[df['max_salary'].notna() & (df['max_salary'] > 0) & (df['max_salary'] < 500000)]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Salary", f"${salary_df['max_salary'].mean():,.0f}")
    col2.metric("Median Salary", f"${salary_df['max_salary'].median():,.0f}")
    col3.metric("Jobs with Salary Data", f"{len(salary_df):,}")
    
    st.markdown("---")
    
    # Salary by skill
    st.subheader("Average Salary by Tech Skill")
    
    skill_salaries = {}
    for skill in TECH_SKILLS:
        skill_jobs = salary_df[salary_df['tech_skills'].apply(lambda x: skill in x)]
        if len(skill_jobs) >= 50:
            skill_salaries[skill] = skill_jobs['max_salary'].mean()
    
    sorted_salaries = sorted(skill_salaries.items(), key=lambda x: x[1], reverse=True)[:15]
    
    fig = px.bar(x=[x[1] for x in sorted_salaries], y=[x[0] for x in sorted_salaries],
                 orientation='h', color=[x[1] for x in sorted_salaries],
                 color_continuous_scale='oranges',
                 labels={'x': 'Average Salary ($)', 'y': 'Skill'})
    fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============ JOB RECOMMENDATIONS PAGE ============
elif page == "Job Recommendations":
    st.header("Job Recommendations")
    
    st.markdown("Enter your skills to find matching jobs.")
    
    # Skill selection
    user_skills = st.multiselect(
        "Select your skills:",
        options=sorted(TECH_SKILLS),
        default=['python', 'sql']
    )
    
    if user_skills and st.button("Find Jobs", type="primary"):
        # Calculate match scores
        def match_score(job_skills):
            if not job_skills:
                return 0
            return sum(1 for skill in user_skills if skill in job_skills)
        
        df['match_score'] = df['tech_skills'].apply(match_score)
        top_jobs = df[df['match_score'] > 0].nlargest(10, 'match_score')
        
        st.subheader(f"Top 10 Jobs Matching Your Skills")
        
        for i, (_, job) in enumerate(top_jobs.iterrows(), 1):
            matching = [s for s in user_skills if s in job['tech_skills']]
            
            with st.expander(f"{i}. {job['title']} at {job['company_name']}"):
                col1, col2 = st.columns(2)
                col1.write(f"**Location:** {job['location']}")
                col1.write(f"**Experience:** {job['formatted_experience_level']}")
                col2.write(f"**Match Score:** {job['match_score']}/{len(user_skills)}")
                col2.write(f"**Matching Skills:** {', '.join(matching)}")
                
                if pd.notna(job['max_salary']) and job['max_salary'] > 0:
                    st.write(f"**Salary:** ${job['max_salary']:,.0f}")

# ============ SKILLS GAP ANALYSIS PAGE ============
elif page == "Skills Gap Analysis":
    st.header("Skills Gap Analysis")
    
    st.markdown("Find out what skills you need to learn for your dream job.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_skills = st.multiselect(
            "Your current skills:",
            options=sorted(TECH_SKILLS),
            default=['python', 'sql', 'excel']
        )
    
    with col2:
        target_job = st.text_input("Target job title:", value="data scientist")
    
    if user_skills and target_job and st.button("Analyze Gap", type="primary"):
        # Find target jobs
        target_jobs = df[df['title'].str.lower().str.contains(target_job.lower(), na=False)]
        
        if len(target_jobs) == 0:
            st.error(f"No jobs found with title containing '{target_job}'")
        else:
            st.success(f"Found {len(target_jobs)} jobs matching '{target_job}'")
            
            # Collect skills from target jobs
            all_skills = []
            for skills in target_jobs['tech_skills']:
                all_skills.extend(skills)
            skill_counts = Counter(all_skills)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Skills You Have")
                have_data = []
                for skill in user_skills:
                    if skill in skill_counts:
                        have_data.append({'Skill': skill, 'Jobs Requiring': skill_counts[skill]})
                
                if have_data:
                    have_df = pd.DataFrame(have_data).sort_values('Jobs Requiring', ascending=False)
                    st.dataframe(have_df, use_container_width=True)
                else:
                    st.write("None of your skills match this job type.")
            
            with col2:
                st.subheader("Skills to Learn")
                missing_data = []
                for skill, count in skill_counts.most_common(15):
                    if skill not in user_skills:
                        missing_data.append({'Skill': skill, 'Jobs Requiring': count})
                
                if missing_data:
                    missing_df = pd.DataFrame(missing_data)
                    st.dataframe(missing_df, use_container_width=True)

# Footer
st.sidebar.markdown("---")

st.sidebar.markdown("**Disclaimer:** For educational purposes only.")
