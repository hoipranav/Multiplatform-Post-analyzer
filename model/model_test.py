import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

model = joblib.load('./analyzer/model/language_detector.pkl')
cv = joblib.load('./analyzer/model/cv.pkl')

comment = ["505mereko bss thugsena pta h awwww"]

final_comment = cv.transform(comment)

print(model.predict_proba(final_comment))
print(model.predict(final_comment))