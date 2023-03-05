# “Analysis of comments from news in the oil industry for the formation of trends using NLP”

classification_parsing_comments_and_graphics_output.py - Classification of comments received by parsing the site, output of a graph with a change in tonality for the top 15 tags.
model_bert_nlp_ver_final_ipynb_.py - BERT machine learning model
parsing_NLP_comments.py - Parsing comments and tags from a news portal 
parsing_NLP_news_url.py - Parsing links to news
word_processing_nlp_ver_final.py - Preprocessing a dataset with 26,000 comments

# Team 
• Zbrodov Evgeny Alekseevich (@Y0uGeeN):
Data analysis, data preprocessing, model creation, report writing, data visualization

• Odinaev Georgy Andreevich:
Data analysis, data preprocessing, model creation, report writing, data visualization

• Pyatanov Kirill Andreevich: 
Data collection, data preprocessing, model testing, selection of hyperparameters

# Topic description
Analysis of people's comments from news related to the oil industry, where the spectrum of users' attitudes to news is evaluated for the formation of oil market trends in a certain period of time.

![image](https://user-images.githubusercontent.com/89632164/222968977-9398c7e2-f65c-47a9-9552-b4d73f9f5a18.png)

This can help companies understand public opinion about the market situation and take any action more quickly.

We took a dataset with comments, performed work on describing the mood of the comment and divided it into 5 classes from the most negative to the most positive ( -2,-1,0,1,2 ) where -2 is a negative comment, 0 is neutral, 2 is positive. 

Next, we take a news portal where there are news about oil, comments and tags to the news. 

We take tags and comments to the news with the help of parsing and analyze the mood of users. Then we build statistics on the connection of tags and the mood of comments.
As a result, we get several graphs of the most popular information guides and user reactions to them.

![image](https://user-images.githubusercontent.com/89632164/222969131-885eb194-e6a7-4ec5-8695-e09111048e78.png)
