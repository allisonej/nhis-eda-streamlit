# -*- coding:utf-8 -*-

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("BMI(Body Mess Index, 체질량지수) 랭크 확인하기")
st.write("이 페이지에서는 개인 BMI의 위치를 확인합니다.")

col_1, col_2 = st.columns(2)

with col_1:
    # 연도 - 라디오 버튼
    input_year = st.radio("확인 년도를 선택하세요.",
            ('2018', '2019', '2020', '2021', '2022'))
    if input_year == '2018':
        input_year = 2018
    elif input_year == '2019':
        input_year = 2019
    elif input_year == '2020':
        input_year = 2020
    elif input_year == '2021':
        input_year = 2021
    else:
        input_year = 2022

with col_2:
    # # 성별 - 라디오 버튼
    input_sex = st.radio(
        '확인할 성별을 확인하세요.',
        ('남성', '여성', '전체데이터에서 보기'))

# 나이 - 숫자 입력
input_age = st.number_input(
    label='나이를 입력해 주세요. (20~90)',
    min_value=20, 
    max_value=90, 
    value=30,
)
input_age = input_age//5+1 #27세면 나이구간 6 (25~30), 코드구간: 5~18 (20~90)
if input_age>=18:
    st.write('당신이 입력하신 :red[나이대]는:  ', input_age*5-5, '~')
else:
    st.write('당신이 입력하신 :red[나이대]는:  ', input_age*5-5, '~', input_age*5-1)

col1, col2 = st.columns(2)

with col1:
    # 키 - 숫자 입력
    input_height = st.number_input(
        label='키(cm)를 입력해 주세요.',
        min_value=45, 
        max_value=300, 
        value=165,
    )
    st.write('당신이 입력하신 :red[키]는:  ', input_height, 'cm')


with col2:

    # 체중 - 숫자 입력
    input_weight = st.number_input(
        label='체중(kg)를 입력해 주세요.',
        min_value=20, 
        max_value=300, 
        value=65,
    )
    st.write('당신이 입력하신 :red[체중]은:  ', input_weight, 'kg')

# 완료 버튼 클릭
button = st.button('BMI를 체크합니다.')


if button:
    target_bmi = input_weight / ( input_height / 100 ) ** 2
    # bmi 구간별로 색 다르게
    if target_bmi<18.5:
        #저체중
        st.write(f'BMI는 :blue[{target_bmi:.2f} 저체중]입니다 :sparkles:')
    elif 18.5<=target_bmi and target_bmi<25:
        #정상
        st.write(f'BMI는 :green[{target_bmi:.2f} 정상]입니다 :sparkles:')
    elif 25<=target_bmi and target_bmi<30:
        #과체중
        st.write(f'BMI는 :orange[{target_bmi:.2f} 과체중]입니다 :sparkles:')
    elif 30<=target_bmi and target_bmi<35:
        #비만1
        st.write(f'BMI는 :red[{target_bmi:.2f} 비만1]입니다 :sparkles:')
    elif 35<=target_bmi and target_bmi<40:
        #비만2
        st.write(f'BMI는 :red[{target_bmi:.2f} 비만2]입니다 :sparkles:')
    else:
        #비만3
        st.write(f'BMI는 :red[{target_bmi:.2f} 비만3]입니다 :sparkles:')
    # st.write(f'BMI는 :blue[{target_bmi:.2f}] 이입니다 :sparkles:')

    # 버튼 누르고 대기하게 만들기 [주의] 데이터 입력했을때 안꼬일까?
    # 연도별로 경량된 데이터 로드
    import pandas as pd

    pd.option_context('mode.use_inf_as_na', True)
    tmp = pd.read_csv(f'shortened_data_{input_year}.csv')
    # 연령대 코드 필터링
    # input_age
    tmp = tmp[tmp['age']==input_age][['height', 'weight', 'sex']]
    # st.table(tmp.head()) #필터링 확인 ok


    # 성별필터링
    # 전체 데이터일 경우에 필터링 안함
    if input_sex == "남성":
        tmp = tmp[tmp['sex']==1][['height', 'weight']]
    elif input_sex == "여성":
        tmp = tmp[tmp['sex']==2][['height', 'weight']]
    else:
        tmp = tmp['height', 'weight']
    
    # 데이터셋의 BMI 계산
    tmp['BMI'] = tmp['weight'] / ( tmp['height'] / 100 ) ** 2

    # 찾고자 하는 값이 몇 퍼센트에 해당하는지 계산
    percentile = ( tmp['BMI'] < target_bmi ).sum() / len( tmp ) * 100

    st.write(f":blue[{target_bmi:.2f}]는 나이, 성별이 고려된 데이터셋에서 상위 약 :blue[{percentile:.2f}] 퍼센트에 해당합니다.")
    st.caption("BMI가 낮을수록 건강상 이점이 있을 가능성이 높으므로 상위로 표현하였습니다.")

    # 결과탭; 즉, BUTTON누른 후 유효
    # 연도, 나이, 성별, 
    # 탭1 : 키, 체중
    # 탭2 : bmi
    # 첫 번째 탭: 키와 체중 그래프

    # 탭을 추가
    tab1, tab2 = st.tabs(['Height vs. Weight', 'BMI Distribution'])
    
    with tab1:
        st.write("## Height vs. Weight")
        # 플롯 그리기
        tab1_plot = st.caption("처리에 시간이 걸리니 기다려 주세요...")
        
        fig, ax = plt.subplots()
        sns.scatterplot(x='height', y='weight', data=tmp, label='Data Points')
        ax.scatter(input_height, input_weight, color='red', label='Your Data')

        # 사용자 BMI 표시
        ax.text(input_height + 1, input_weight - 5, f'BMI: {target_bmi:.2f}', fontsize=10, ha='left')

        ax.set_xlabel('Height (5cm)')
        ax.set_ylabel('Weight (5kg)')
        ax.set_title('Height vs. Weight')

        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        tab1_col1, tab1_col2 = st.columns(2)
        with tab1_col1:
            st.write(tmp['height'].describe()) 
        with tab1_col2:
            st.write(tmp['weight'].describe())

    # 두 번째 탭: BMI 그래프

    with tab2:
        st.write("## BMI Distribution")
        # 플롯 그리기
        fig, ax = plt.subplots()
        sns.histplot(tmp['BMI'], kde=True, ax=ax)
        ax.axvline(target_bmi, color='red', linestyle='--', label='Your BMI')
        ax.set_xlabel('BMI')
        ax.set_ylabel('Frequency')
        ax.set_title('BMI Distribution')
        ax.legend()
        ax.text(target_bmi, len(tmp)/(max(tmp['BMI'])-min(tmp['BMI'])), f'Your BMI: {target_bmi:.2f}', fontsize=10, ha='center', va='top')
        st.pyplot(fig)
