import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from catboost import CatBoostClassifier


df = pd.read_excel('customer.xlsx')


df_sales = pd.read_csv('sales.csv').rename(columns={'CustomerID':'customerid'})
df_sales['spend'] = df_sales['UnitPrice']*df_sales['Quantity']
df_sales = df_sales.groupby(['customerid'])['spend'].sum().reset_index()
df =df.merge(df_sales,on='customerid',)

print(df.isna().sum())

cat_features = df.columns.difference(pd.Index(['customerid','churn','engagementscore','rfmservice','seniorcitizen','spend','tenure'])).tolist()
num_features = ['engagementscore','rfmservice','seniorcitizen','spend','tenure']
features = cat_features + num_features
target='churn'
df[target] = df[target].map({'Yes':1,'No':0})

print(df[features].describe())

#import pdb;pdb.set_trace()
clf  = CatBoostClassifier(iterations=10_000,verbose=1,learning_rate=0.01)
clf.fit(df[features],df[target],cat_features=cat_features)
df['proba'] = clf.predict(df[features],prediction_type='Probability')[:,1]
df['churn_pred']=df['proba'].map(lambda x:0 if x<=0.5 else 1)
print(classification_report(df['churn'],df['churn_pred']))

df[['customerid','gender']+num_features+['churn','proba','churn_pred']].to_csv('predictions.csv',index=False)

#print('Mean Accuracy ',clf.score(df[features],df[target]))
