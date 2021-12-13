import streamlit as st
import pandas as pd
import plotly.express as px
from numpy import dot
from numpy.linalg import norm

import json

def readData(fileName):
	df = pd.read_csv("data/" + fileName + "_topic.csv")
	df["tweet_time"] = df["tweet_time"].astype("datetime64")
	return df

def plotAnalysis(fileName):
	df= readData(fileName)

	df2= readData(fileName+'_real')

	# %%

	topics_cols = []
	with open("data/keywords.json", "r") as read_file:
		_topics_cols = list(json.load(read_file))
		for x in _topics_cols:
			if ((x in df.columns) or (x in df2.columns)):
				topics_cols.append(x)
				if (x not in df.columns):
					df[x] = None
				if (x not in df2.columns):
					df2[x] = None

	# ax = df[topics_cols].groupby(df["tweet_time"].dt.date).count().plot(kind="bar",stacked=True,figsize=(10,8))
	# ax.figure.savefig('demo-file.pdf')

	drawData = df[topics_cols][df[topics_cols] > 0]
	drawData2 = df2[topics_cols][df2[topics_cols] > 0]
	List1 = drawData.count()
	List2 = drawData2.count()
	sim = dot(List1, List2) / (norm(List1) * norm(List2))
	st.header("Topic from " + fileName )
	st.markdown("**Similarity = "+'{:.2f}%'.format(sim*100)+"**")

	# Create distplot with custom bin_size
	# disData = (drawData.count()/sum(drawData.count())).reset_index().rename(columns={0:'fake'}).merge((drawData2.count()/sum(drawData2.count())).reset_index().rename(columns={0:'real'})).set_index('index');
	disData = (List1*100/sum(List1)).reset_index().rename(columns={0:'fake'}).merge((List2*100/sum(List2)).reset_index().rename(columns={0:'real'}));

	# st.write(disData)
	# st.write(pd.concat([drawData.count().reset_index().rename(columns={0:'fake'}),drawData2.count().reset_index().rename(columns={0:'real'})]))

	fig = px.bar(disData, x="index", y=["fake","real"], barmode='group',labels={'value':'Percentage','index':'topic'})

	st.subheader(f'Fake news ({df.shape[0]} posts)')
	st.plotly_chart(px.bar(List1,labels={'value':'Post','index':'topic'},title="Fake news"),use_container_width=True)
	st.subheader(f'Real news ({df2.shape[0]} posts)')
	st.plotly_chart(px.bar(List2,labels={'value':'Post','index':'topic'},title="Real news"),use_container_width=True)
	st.plotly_chart(fig,use_container_width=True)

	delta = (List1*100/sum(List1))-(List2*100/sum(List2))
	st.plotly_chart(px.bar(delta.reset_index(), x="index", y=0, labels={'0':'Percentage','index':'topic'},title="Different"),use_container_width=True)


	# %%
	return df



st.set_page_config(
	 page_title="Topics Dictionary",
	 page_icon="random",
	 layout="wide",
	 initial_sidebar_state="expanded",
 )



st.title('Topics Using Dictionary')
st.write("Last Updated: Dec 12, 2021")



for fileID in ["FNsample1","FNsample2","FNsample3","FNsample4"]:

	plotAnalysis(fileID)

	# if len(target_tweet)>0:
	# 	st.markdown("**All texts (Tweet content, article content,...) after processing:** " + processed_text)
	#
	# for i in range(n_tops):
	# 	st.write("-------")
	# 	st.markdown(f"**Topic {i+1}:** "+ str(df[df["tweetid"]==tweetid][f"top{i+1}"].values[0]))
	# 	all_keywords_in_the_topic = topics_dict[df[df["tweetid"]==tweetid][f"top{i+1}"].values[0]]
	# 	st.markdown("**Keywords appearing:** "+ get_num_words(processed_text, all_keywords_in_the_topic,return_keys=True))
	# 	st.write("-------")














