import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st


st.set_page_config(page_title='시각화 라이브러리 비교', page_icon='📊', layout='wide')

st.title('시각화 라이브러리 비교')
st.write('같은 예시 데이터를 Matplotlib, Seaborn, Plotly로 각각 표현합니다.')

months = list(range(1, 13))
month_names = [
	'1월', '2월', '3월', '4월', '5월', '6월',
	'7월', '8월', '9월', '10월', '11월', '12월',
]
temperature_data = pd.DataFrame({
	'월': month_names * 3,
	'월 번호': months * 3,
	'지역': ['서울'] * 12 + ['부산'] * 12 + ['제주'] * 12,
	'평균 기온 (°C)': [
		-2, 1, 6, 13, 19, 23, 26, 27, 22, 15, 7, 0,
		4, 6, 10, 15, 19, 22, 25, 27, 23, 18, 12, 7,
		6, 7, 10, 14, 18, 22, 26, 28, 24, 19, 14, 9,
	],
})

sales_data = pd.DataFrame({
	'분기': ['1분기', '2분기', '3분기', '4분기'] * 3,
	'분기 번호': [1, 2, 3, 4] * 3,
	'상품': ['음료'] * 4 + ['디저트'] * 4 + ['식사'] * 4,
	'매출 (만원)': [320, 410, 530, 470, 250, 360, 440, 520, 480, 510, 590, 680],
})


def show_temperature_charts(data):
	chart_columns = st.columns(3)

	with chart_columns[0]:
		st.caption('Matplotlib')
		figure, axis = plt.subplots(figsize=(7, 4))
		for region, region_data in data.groupby('지역', sort=False):
			axis.plot(region_data['월 번호'], region_data['평균 기온 (°C)'], marker='o', label=region)
		axis.set_title('지역별 월평균 기온')
		axis.set_xlabel('월')
		axis.set_ylabel('평균 기온 (°C)')
		axis.set_xticks(months, month_names)
		axis.legend(title='지역')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	with chart_columns[1]:
		st.caption('Seaborn')
		figure, axis = plt.subplots(figsize=(7, 4))
		sns.lineplot(
			data=data,
			x='월 번호',
			y='평균 기온 (°C)',
			hue='지역',
			marker='o',
			ax=axis,
		)
		axis.set_title('지역별 월평균 기온')
		axis.set_xlabel('월')
		axis.set_ylabel('평균 기온 (°C)')
		axis.set_xticks(months, month_names)
		axis.legend(title='지역')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	chart_columns[2].caption('Plotly')
	figure = px.line(
		data,
		x='월 번호',
		y='평균 기온 (°C)',
		color='지역',
		markers=True,
		title='지역별 월평균 기온',
		labels={'월 번호': '월', '평균 기온 (°C)': '평균 기온 (°C)', '지역': '지역'},
		hover_data={'월': True, '월 번호': False},
	)
	figure.update_xaxes(tickmode='array', tickvals=months, ticktext=month_names)
	chart_columns[2].plotly_chart(figure, width='stretch')


def show_sales_charts(data):
	chart_columns = st.columns(3)

	with chart_columns[0]:
		st.caption('Matplotlib')
		figure, axis = plt.subplots(figsize=(7, 4))
		for product, product_data in data.groupby('상품', sort=False):
			axis.plot(product_data['분기 번호'], product_data['매출 (만원)'], marker='o', label=product)
		axis.set_title('상품별 분기 매출')
		axis.set_xlabel('분기')
		axis.set_ylabel('매출 (만원)')
		axis.set_xticks([1, 2, 3, 4], ['1분기', '2분기', '3분기', '4분기'])
		axis.legend(title='상품')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	with chart_columns[1]:
		st.caption('Seaborn')
		figure, axis = plt.subplots(figsize=(7, 4))
		sns.barplot(data=data, x='분기', y='매출 (만원)', hue='상품', ax=axis)
		axis.set_title('상품별 분기 매출')
		axis.set_xlabel('분기')
		axis.set_ylabel('매출 (만원)')
		axis.legend(title='상품')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	chart_columns[2].caption('Plotly')
	figure = px.bar(
		data,
		x='분기',
		y='매출 (만원)',
		color='상품',
		barmode='group',
		category_orders={'분기': ['1분기', '2분기', '3분기', '4분기']},
		title='상품별 분기 매출',
		labels={'분기': '분기', '매출 (만원)': '매출 (만원)', '상품': '상품'},
	)
	chart_columns[2].plotly_chart(figure, width='stretch')


st.header('예시 1. 지역별 월평균 기온', divider='gray')
st.caption('계절에 따른 서울, 부산, 제주 지역의 월평균 기온을 비교합니다.')
show_temperature_charts(temperature_data)
with st.expander('기온 예시 데이터 보기'):
	st.dataframe(temperature_data, hide_index=True, width='stretch')

st.header('예시 2. 상품별 분기 매출', divider='gray')
st.caption('음료, 디저트, 식사의 분기별 매출을 비교합니다.')
show_sales_charts(sales_data)
with st.expander('매출 예시 데이터 보기'):
	st.dataframe(sales_data, hide_index=True, width='stretch')
