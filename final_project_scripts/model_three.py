from xgboost import XGBClassifier

# train and fit the model
xgb_model = XGBClassifier(objective='multi:softmax', num_class=len(label_encoder.classes_), random_state=1)
xgb_model.fit(X_train, y_train)

# make predictions on test
y_pred = xgb_model.predict(X_test)

# evaluate the model
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

print("\nAccuracy Score:")
print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test, y_pred), display_labels=label_encoder.classes_)
disp.plot(cmap=plt.cm.Blues, values_format='d')
plt.title("Confusion Matrix")
plt.show()

# CV scores
xgb_scores = cross_val_score(xgb_model, X, y, cv=5, scoring='accuracy')
print(f"XGBoost CV Scores: {xgb_scores}")
print(f"Average XGBoost Accuracy: {xgb_scores.mean():.4f}")
