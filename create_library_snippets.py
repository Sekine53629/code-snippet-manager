#!/usr/bin/env python3
"""
Create Library Snippets

Adds common code snippets for popular Python libraries:
- NumPy
- Matplotlib
- Pandas
- scikit-learn
- TensorFlow/Keras
- Django
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import load_config
from utils.database import DatabaseManager


def create_library_snippets(db_manager: DatabaseManager):
    """Create snippets for popular Python libraries."""

    print("Creating library snippets...")
    print("=" * 60)

    # ========================================
    # NumPy Snippets
    # ========================================
    print("\n[1/6] Creating NumPy snippets...")
    numpy_tag_id = db_manager.get_or_create_tag("NumPy", parent_id=None, tag_type="folder")

    numpy_snippets = [
        {
            "name": "Array Creation",
            "code": """import numpy as np

# Create arrays
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.zeros((3, 4))
arr3 = np.ones((2, 3))
arr4 = np.arange(0, 10, 2)
arr5 = np.linspace(0, 1, 5)""",
            "language": "python",
            "description": "Various ways to create NumPy arrays",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Array Operations",
            "code": """import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# Basic operations
print(arr.shape)      # (2, 3)
print(arr.ndim)       # 2
print(arr.dtype)      # int64
print(arr.sum())      # 21
print(arr.mean())     # 3.5
print(arr.max())      # 6""",
            "language": "python",
            "description": "Common NumPy array operations and properties",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Array Indexing and Slicing",
            "code": """import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Indexing
print(arr[0, 1])      # 2
print(arr[1])         # [4, 5, 6]

# Slicing
print(arr[:2, 1:])    # [[2, 3], [5, 6]]
print(arr[::2, ::2])  # [[1, 3], [7, 9]]

# Boolean indexing
print(arr[arr > 5])   # [6, 7, 8, 9]""",
            "language": "python",
            "description": "NumPy array indexing and slicing techniques",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Matrix Operations",
            "code": """import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
C = np.dot(A, B)
# or
C = A @ B

# Transpose
A_T = A.T

# Inverse
A_inv = np.linalg.inv(A)

# Determinant
det = np.linalg.det(A)""",
            "language": "python",
            "description": "Linear algebra operations with NumPy",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Random Numbers",
            "code": """import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Random integers
rand_int = np.random.randint(0, 10, size=(3, 3))

# Random floats [0, 1)
rand_float = np.random.random((3, 3))

# Normal distribution
normal = np.random.randn(1000)

# Choice
choice = np.random.choice([1, 2, 3, 4, 5], size=10)""",
            "language": "python",
            "description": "Generate random numbers with NumPy",
            "tag_ids": [numpy_tag_id]
        }
    ]

    for snippet in numpy_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(numpy_snippets)} NumPy snippets")

    # ========================================
    # Matplotlib Snippets
    # ========================================
    print("\n[2/6] Creating Matplotlib snippets...")
    matplotlib_tag_id = db_manager.get_or_create_tag("Matplotlib", parent_id=None, tag_type="folder")

    matplotlib_snippets = [
        {
            "name": "Basic Line Plot",
            "code": """import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Sine Wave')
plt.legend()
plt.grid(True)
plt.show()""",
            "language": "python",
            "description": "Create a basic line plot with Matplotlib",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Scatter Plot",
            "code": """import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)
sizes = 1000 * np.random.rand(100)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot')
plt.show()""",
            "language": "python",
            "description": "Create scatter plot with color mapping",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Subplots",
            "code": """import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('sin(x)')

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title('cos(x)')

axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_title('tan(x)')

axes[1, 1].plot(x, x**2)
axes[1, 1].set_title('x²')

plt.tight_layout()
plt.show()""",
            "language": "python",
            "description": "Create multiple subplots in a grid",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Bar Chart",
            "code": """import matplotlib.pyplot as plt

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

plt.figure(figsize=(10, 6))
plt.bar(categories, values, color='skyblue', edgecolor='navy')
plt.xlabel('Category')
plt.ylabel('Value')
plt.title('Bar Chart Example')
plt.grid(axis='y', alpha=0.3)
plt.show()""",
            "language": "python",
            "description": "Create a bar chart",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Histogram",
            "code": """import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.grid(axis='y', alpha=0.3)
plt.show()""",
            "language": "python",
            "description": "Create a histogram",
            "tag_ids": [matplotlib_tag_id]
        }
    ]

    for snippet in matplotlib_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(matplotlib_snippets)} Matplotlib snippets")

    # ========================================
    # Pandas Snippets
    # ========================================
    print("\n[3/6] Creating Pandas snippets...")
    pandas_tag_id = db_manager.get_or_create_tag("Pandas", parent_id=None, tag_type="folder")

    pandas_snippets = [
        {
            "name": "DataFrame Creation",
            "code": """import pandas as pd

# From dictionary
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Tokyo', 'Osaka', 'Kyoto']
})

# From CSV
df = pd.read_csv('data.csv')

# From Excel
df = pd.read_excel('data.xlsx')

print(df.head())""",
            "language": "python",
            "description": "Various ways to create Pandas DataFrames",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Inspection",
            "code": """import pandas as pd

# Basic info
print(df.shape)           # (rows, columns)
print(df.info())          # Data types and non-null counts
print(df.describe())      # Statistical summary
print(df.head(10))        # First 10 rows
print(df.tail(10))        # Last 10 rows

# Column info
print(df.columns)         # Column names
print(df.dtypes)          # Data types
print(df.isnull().sum())  # Missing values per column""",
            "language": "python",
            "description": "Inspect DataFrame structure and content",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Selection",
            "code": """import pandas as pd

# Select columns
df['column_name']
df[['col1', 'col2']]

# Select rows by index
df.iloc[0]           # First row
df.iloc[0:5]         # First 5 rows
df.iloc[:, 0:3]      # First 3 columns

# Select by label
df.loc[0, 'column_name']
df.loc[:, ['col1', 'col2']]

# Conditional selection
df[df['age'] > 30]
df[(df['age'] > 25) & (df['city'] == 'Tokyo')]""",
            "language": "python",
            "description": "Select and filter DataFrame data",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Cleaning",
            "code": """import pandas as pd

# Handle missing values
df.dropna()                    # Drop rows with NaN
df.fillna(0)                   # Fill NaN with 0
df.fillna(df.mean())          # Fill with mean

# Remove duplicates
df.drop_duplicates()

# Rename columns
df.rename(columns={'old_name': 'new_name'})

# Change data types
df['column'] = df['column'].astype('int')

# Replace values
df['column'].replace({'old': 'new'})""",
            "language": "python",
            "description": "Clean and prepare DataFrame data",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "GroupBy and Aggregation",
            "code": """import pandas as pd

# Group by single column
grouped = df.groupby('category')
print(grouped.mean())
print(grouped.sum())
print(grouped.count())

# Group by multiple columns
grouped = df.groupby(['category', 'region'])

# Multiple aggregations
result = df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': ['sum', 'mean']
})

print(result)""",
            "language": "python",
            "description": "Group and aggregate DataFrame data",
            "tag_ids": [pandas_tag_id]
        }
    ]

    for snippet in pandas_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(pandas_snippets)} Pandas snippets")

    # ========================================
    # scikit-learn Snippets
    # ========================================
    print("\n[4/6] Creating scikit-learn snippets...")
    sklearn_tag_id = db_manager.get_or_create_tag("scikit-learn", parent_id=None, tag_type="folder")

    sklearn_snippets = [
        {
            "name": "Train-Test Split",
            "code": """from sklearn.model_selection import train_test_split

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% for testing
    random_state=42,    # For reproducibility
    stratify=y          # Maintain class distribution
)

print(f"Train size: {len(X_train)}")
print(f"Test size: {len(X_test)}")""",
            "language": "python",
            "description": "Split dataset into training and testing sets",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "Linear Regression",
            "code": """from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"R² Score: {r2:.4f}")""",
            "language": "python",
            "description": "Train and evaluate Linear Regression model",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "Random Forest Classifier",
            "code": """from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Create and train model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print(classification_report(y_test, y_pred))""",
            "language": "python",
            "description": "Train Random Forest classifier",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "StandardScaler",
            "code": """from sklearn.preprocessing import StandardScaler

# Create scaler
scaler = StandardScaler()

# Fit and transform training data
X_train_scaled = scaler.fit_transform(X_train)

# Transform test data (use same scaler!)
X_test_scaled = scaler.transform(X_test)

# The scaler can be saved for later use
import joblib
joblib.dump(scaler, 'scaler.pkl')
loaded_scaler = joblib.load('scaler.pkl')""",
            "language": "python",
            "description": "Standardize features using StandardScaler",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "Cross-Validation",
            "code": """from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)

# Perform 5-fold cross-validation
scores = cross_val_score(
    model, X, y,
    cv=5,                    # 5 folds
    scoring='accuracy'       # Metric
)

print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.4f}")
print(f"Std: {scores.std():.4f}")""",
            "language": "python",
            "description": "Perform cross-validation",
            "tag_ids": [sklearn_tag_id]
        }
    ]

    for snippet in sklearn_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(sklearn_snippets)} scikit-learn snippets")

    # ========================================
    # TensorFlow/Keras Snippets
    # ========================================
    print("\n[5/6] Creating TensorFlow/Keras snippets...")
    tf_tag_id = db_manager.get_or_create_tag("TensorFlow/Keras", parent_id=None, tag_type="folder")

    tf_snippets = [
        {
            "name": "Sequential Model",
            "code": """from tensorflow import keras
from tensorflow.keras import layers

# Create Sequential model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(input_dim,)),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())""",
            "language": "python",
            "description": "Create a Sequential neural network model",
            "tag_ids": [tf_tag_id]
        },
        {
            "name": "CNN for Image Classification",
            "code": """from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)""",
            "language": "python",
            "description": "Create CNN for image classification",
            "tag_ids": [tf_tag_id]
        },
        {
            "name": "Model Training",
            "code": """# Train the model
history = model.fit(
    X_train, y_train,
    batch_size=32,
    epochs=10,
    validation_split=0.2,
    callbacks=[
        keras.callbacks.EarlyStopping(
            patience=3,
            restore_best_weights=True
        ),
        keras.callbacks.ModelCheckpoint(
            'best_model.h5',
            save_best_only=True
        )
    ]
)

# Evaluate
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_acc:.4f}")""",
            "language": "python",
            "description": "Train Keras model with callbacks",
            "tag_ids": [tf_tag_id]
        },
        {
            "name": "Save and Load Model",
            "code": """from tensorflow import keras

# Save entire model
model.save('my_model.h5')

# Load model
loaded_model = keras.models.load_model('my_model.h5')

# Save only weights
model.save_weights('model_weights.h5')

# Load weights
model.load_weights('model_weights.h5')

# Make predictions
predictions = loaded_model.predict(X_new)""",
            "language": "python",
            "description": "Save and load Keras models",
            "tag_ids": [tf_tag_id]
        }
    ]

    for snippet in tf_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(tf_snippets)} TensorFlow/Keras snippets")

    # ========================================
    # Django Snippets
    # ========================================
    print("\n[6/6] Creating Django snippets...")
    django_tag_id = db_manager.get_or_create_tag("Django", parent_id=None, tag_type="folder")

    django_snippets = [
        {
            "name": "Model Definition",
            "code": """from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title""",
            "language": "python",
            "description": "Define Django model with relationships",
            "tag_ids": [django_tag_id]
        },
        {
            "name": "Class-Based View",
            "code": """from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(published=True)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content', 'published']
    success_url = reverse_lazy('article-list')""",
            "language": "python",
            "description": "Django class-based views (CBVs)",
            "tag_ids": [django_tag_id]
        },
        {
            "name": "URL Patterns",
            "code": """from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='delete'),
]""",
            "language": "python",
            "description": "Define URL patterns for Django app",
            "tag_ids": [django_tag_id]
        },
        {
            "name": "Django REST Framework ViewSet",
            "code": """from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Article.objects.all()
        published = self.request.query_params.get('published')
        if published is not None:
            queryset = queryset.filter(published=published)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)""",
            "language": "python",
            "description": "Django REST Framework ViewSet",
            "tag_ids": [django_tag_id]
        },
        {
            "name": "Django Forms",
            "code": """from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            }),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters')
        return title""",
            "language": "python",
            "description": "Django ModelForm with validation",
            "tag_ids": [django_tag_id]
        }
    ]

    for snippet in django_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(django_snippets)} Django snippets")

    # ========================================
    # Summary
    # ========================================
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    total = len(numpy_snippets) + len(matplotlib_snippets) + len(pandas_snippets) + \
            len(sklearn_snippets) + len(tf_snippets) + len(django_snippets)
    print(f"✅ Created {total} library snippets:")
    print(f"   - NumPy: {len(numpy_snippets)}")
    print(f"   - Matplotlib: {len(matplotlib_snippets)}")
    print(f"   - Pandas: {len(pandas_snippets)}")
    print(f"   - scikit-learn: {len(sklearn_snippets)}")
    print(f"   - TensorFlow/Keras: {len(tf_snippets)}")
    print(f"   - Django: {len(django_snippets)}")
    print("\nYou can now find these snippets in the application!")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Code Snippet Manager - Library Snippets Creator")
    print("=" * 60)

    # Load configuration
    config = load_config()

    # Initialize database
    db_manager = DatabaseManager(config)

    # Create library snippets
    create_library_snippets(db_manager)

    print("\n✅ Done!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
