import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train_decision_model(X,y, save_path="models/decision_model.pkl"):
    model=LogisticRegression()
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=42)

    model.fit(X_train,y_train)

    joblib.dump(model, save_path)

    return {
        "model_path": save_path,
        "accuracy": model.score(X_test, y_test)
    }

def load_model(path="models/decision_model.pkl"):
    return joblib.load(path)
def predict(model, features):
    return model.predict(features)[0]


