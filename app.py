# -*- coding:utf-8 -*-

import streamlit as st

st.title("BMI(Body Mess Index, 체질량지수) 랭크 확인하기")
st.write("이 페이지에서는 개인 BMI의 위치를 확인합니다.")

col_1, col_2 = st.columns(2)

with col_1:
    # 연도 - 라디오 버튼
    input_year = st.radio("확인 년도를 선택하세요.",
            ('2018', '2019', '2020', '2021', '2022'))
with col_2:
    # # 성별 - 라디오 버튼
    # input_sex = st.radio(
    #     '확인할 성별을 확인하세요.',
    #     ('남성', '여성', '무관')
     # 성별 - 라디오 버튼
    input_sex = st.radio(
        '확인할 성별을 확인하세요.',
        ('남성', '여성'))



# 하단은 탭으로 구분

# 나이 - 숫자 입력
input_age = st.number_input(
    label='나이를 입력해 주세요. (20~90)',
    min_value=20, 
    max_value=90, 
    value=30,
)
input_age = input_age//5+1 #27세면 나이구간 6 (25~30)
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
    st.caption("처리에 시간이 걸리니 기다려 주세요...")
    target_bmi = input_weight / ( input_height / 100 ) ** 2
    # bmi 구간별로 색 다르게
    # if bmi<18.5:
    #     #저체중
    # elif 18.5<=bmi and bmi<25:
    #     #정상
    # elif 25<=bmi and bmi<30:
    #     #과체중
    # elif 30<=bmi and bmi<35:
    #     #비만1
    # elif 35<=bmi and bmi<40:
    #     #비만2
    # else:
    #     #비만3
    st.write(f'BMI는 :blue[{target_bmi:.2f}] 이입니다 :sparkles:')

    # 버튼 누르고 대기하게 만들기 [주의] 데이터 입력했을때 안꼬일까?
    import pandas as pd
    tmp = pd.read_csv('shortened_data_2022.csv')
    tmp['BMI'] = tmp['weight'] / ( tmp['height'] / 100 ) ** 2
    
    # 찾고자 하는 값이 몇 퍼센트에 해당하는지 계산
    percentile_value = tmp['BMI'].quantile(q=0.5, interpolation='linear')  # 중간값을 계산합니다.
    percentile = ( tmp['BMI'] < target_bmi ).sum() / len( tmp ) * 100

    st.write(f":blue[{target_bmi:.2f}]는 데이터셋에서 약 :blue[{percentile:.2f}] 퍼센트에 해당합니다.")