# tests/aliases/test_sklearn.py
# C-011: Arabic aliases for scikit-learn

import pathlib

import pytest

sklearn = pytest.importorskip("sklearn", reason="scikit-learn not installed")

import sklearn.cluster as sk_cluster  # noqa: E402
import sklearn.datasets as sk_datasets  # noqa: E402
import sklearn.decomposition as sk_decomposition  # noqa: E402
import sklearn.ensemble as sk_ensemble  # noqa: E402
import sklearn.impute as sk_impute  # noqa: E402
import sklearn.linear_model as sk_linear  # noqa: E402
import sklearn.metrics as sk_metrics  # noqa: E402
import sklearn.model_selection as sk_model_selection  # noqa: E402
import sklearn.pipeline as sk_pipeline  # noqa: E402
import sklearn.preprocessing as sk_preprocessing  # noqa: E402
import sklearn.svm as sk_svm  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def تعلم_الي():
    """Return a ModuleProxy wrapping `sklearn`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("تعلم_آلي", None, None)
    assert spec is not None, "AliasFinder did not find 'تعلم_آلي'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSklearnDatasetsAndModelSelection:
    def test_load_iris_alias(self, تعلم_الي):
        assert تعلم_الي.حمل_ايرس is sk_datasets.load_iris

    def test_train_test_split_alias(self, تعلم_الي):
        assert تعلم_الي.قسم_تدريب_اختبار is sk_model_selection.train_test_split

    def test_cross_val_score_alias(self, تعلم_الي):
        assert تعلم_الي.تحقق_متقاطع is sk_model_selection.cross_val_score

    def test_grid_search_alias(self, تعلم_الي):
        assert تعلم_الي.بحث_شبكي is sk_model_selection.GridSearchCV


class TestSklearnEstimators:
    def test_pipeline_alias(self, تعلم_الي):
        assert تعلم_الي.خط_انابيب is sk_pipeline.Pipeline

    def test_standard_scaler_alias(self, تعلم_الي):
        assert تعلم_الي.مقياس_معياري is sk_preprocessing.StandardScaler

    def test_logistic_regression_alias(self, تعلم_الي):
        assert تعلم_الي.انحدار_لوجستي is sk_linear.LogisticRegression

    def test_random_forest_classifier_alias(self, تعلم_الي):
        assert تعلم_الي.غابه_عشوائيه_مصنف is sk_ensemble.RandomForestClassifier

    def test_svc_alias(self, تعلم_الي):
        assert تعلم_الي.اله_دعم_مصنف is sk_svm.SVC

    def test_simple_imputer_alias(self, تعلم_الي):
        assert تعلم_الي.معوض_بسيط is sk_impute.SimpleImputer

    def test_kmeans_alias(self, تعلم_الي):
        assert تعلم_الي.تجميع_k is sk_cluster.KMeans

    def test_pca_alias(self, تعلم_الي):
        assert تعلم_الي.تحليل_pca is sk_decomposition.PCA


class TestSklearnMetrics:
    def test_accuracy_score_alias(self, تعلم_الي):
        assert تعلم_الي.دقه is sk_metrics.accuracy_score

    def test_classification_report_alias(self, تعلم_الي):
        assert تعلم_الي.تقرير_تصنيف is sk_metrics.classification_report

    def test_mean_squared_error_alias(self, تعلم_الي):
        assert تعلم_الي.خطا_تربيعي_متوسط is sk_metrics.mean_squared_error


class TestSklearnFunctional:
    def test_fit_predict_with_arabic_aliases(self, تعلم_الي):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "sklearn.toml")
        x, y = تعلم_الي.حمل_ايرس(return_X_y=True)
        x_train, x_test, y_train, y_test = تعلم_الي.قسم_تدريب_اختبار(
            x,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y,
        )

        model = تعلم_الي.اصنع_خط_انابيب(
            تعلم_الي.مقياس_معياري(),
            تعلم_الي.انحدار_لوجستي(max_iter=200),
        )
        proxied_model = ClassProxy(model, mapping.attributes)

        proxied_model.درب(x_train, y_train)
        predictions = proxied_model.تنبا(x_test)
        accuracy = تعلم_الي.دقه(y_test, predictions)

        assert accuracy > 0.85
        assert proxied_model.درجه(x_test, y_test) == model.score(x_test, y_test)


class TestSklearnTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "sklearn.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "sklearn"
        assert data["meta"]["arabic_name"] == "تعلم_آلي"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "sklearn.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 35
