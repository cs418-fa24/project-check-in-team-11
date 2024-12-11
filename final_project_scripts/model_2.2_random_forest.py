from sklearn.ensemble import RandomForestClassifier

# initialize and fit on training data
forest = RandomForestClassifier(random_state=1)
forest.fit(X_train, y_train)

# make predictions on test
y_pred = forest.predict(X_test)

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

# CV testing
k = 10
cv_scores = cross_val_score(forest , X, y, cv=k, scoring='accuracy')
print(f"RandomForest CV Scores: {cv_scores}")
print(f"Average accuracy for {k} folds: {cv_scores.mean():.4f}")
