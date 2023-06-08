## rSentimentAnalysis


## 1.	Software Description
   * a. Short name: rSA 
   * b. Full name: Reddit Sentiment Analysis 
   * c. Brief Description with Objectives: rSA will be an application that enables sentiment analysis from the website www.reddit.com. The goal of the application is to provide users with an easy way to analyze the sentiment of comments and posts on various topics. However, our main focus will be on football-related topics, so the functionality will be optimized for sports enthusiasts.
## 2.	Copyright
* a. Authors: Jakub Gabryszewski, Mikołaj Orzoł
* b. Licensing terms: The application is a subject to an open-source license under the MIT License terms.
## 3.	Requirements Specification 
 
| Identifier	| Name |	Description | Priority | Category |
| --------------|-------|------|-----------|-----------|
| REQ-1	| Integration with the Website |	The application should allow the retrieval of comments and posts from the website www.reddit.com. |	High	| Functional |
| REQ-2	| Sentiment Analysis |	The application should allow sentiment analysis of posts and comments.	| High |	Functional |
| REQ-3	| Results Presentation |	The application should present the results of sentiment analysis. | High	| Functional |
| REQ-4	| Error Handling	| The application should display clear error messages in case of any issues with its operation. |	Medium	| Non-Functional |
| REQ-5	| User Interface Language	| The application should have an interface in the English language. |	Medium	| User Interface |
| REQ-6	| Displaying Popular Clubs	| The application should display popular clubs as buttons that redirect to the respective subreddits.  |	Low	| Functional |
| REQ-7 | Post Segmentation by Criteria | The application should allow extraction of paragraphs/titles or images from the text. | Low | Functional |
 
## 4. Development Architecture

| Imports | Description | Command |
| ------- | ---- | --------- |
| Flask | Module required to create an application using the Flask framework. | pip install Flask |
| TextBlob | Module required for language detection, processing, and sentiment analysis of text. | pip install textblob |
| PRAW | Module facilitating the use of the Reddit API. | pip install praw |
