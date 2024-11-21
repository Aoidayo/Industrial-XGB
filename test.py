from xgboost import XGBClassifier

x = [[0, 2],
     [1, 2],
     [0, 3],
     [0, 3]]
y = [0, 0, 1, 1]

params_classifier_fixed = {
    'learning_rate': 0.1,
    'n_estimators': 500,
    'max_depth': 2,
    'objective': 'multi:softmax num_class=n',  # 正确的目标函数
    # 'num_class': 2  # 设置类别数
}

model = XGBClassifier(**params_classifier_fixed)
model.fit(x, y)
