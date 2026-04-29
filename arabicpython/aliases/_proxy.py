"""ModuleProxy — transparent wrapper forwarding attribute access through an Arabic→Python mapping.

Architecture
------------
Four public classes are defined here:

ModuleProxy
    Wraps a Python *module*. Created by AliasFinder; the object a user
    receives after ``استورد فلاسك``. Arabic keys are looked up in the
    mapping dict; unrecognised Arabic raises AttributeError + DeprecationWarning;
    ASCII names fall through to the underlying module.

ClassProxy
    Wraps a Python *object instance* resolved from a module-level alias, such as
    ``flask.request``. Arabic instance attributes are looked up in the mapping's
    ``attributes`` table; unknown names fall through to the real object.

ClassFactory
    Wraps a Python *class* that appears in the mapping's ``proxy_classes`` list.
    When called (``فلاسك.فلاسك(__name__)``), it instantiates the class and
    wraps the result in an InstanceProxy, so Arabic method names work on the
    resulting object.

InstanceProxy
    Wraps a Python *object instance* (e.g. a live Flask app). Resolves
    ``Class.method``-style mapping entries against the real instance:
    ``"طريق" → "Flask.route"`` becomes ``getattr(app, "route")`` (bound).
    Falls through to English for unmapped names; warns + raises for unmapped
    Arabic names that don't correspond to any bound method.
"""

from __future__ import annotations

import types
import warnings
from typing import Any

# Unicode ranges covering Arabic script variants
_ARABIC_RANGES: tuple[tuple[str, str], ...] = (
    ("\u0600", "\u06ff"),  # Arabic
    ("\u0750", "\u077f"),  # Arabic Supplement
    ("\u08a0", "\u08ff"),  # Arabic Extended-A
    ("\ufb50", "\ufdff"),  # Arabic Presentation Forms-A
    ("\ufe70", "\ufeff"),  # Arabic Presentation Forms-B
)


def _is_arabic_looking(name: str) -> bool:
    """Return True if *name* contains at least one Arabic-script character."""
    return any(lo <= ch <= hi for ch in name for lo, hi in _ARABIC_RANGES)


def _is_dunder(name: str) -> bool:
    """Return True for Python's double-underscore protocol names."""
    return len(name) > 4 and name.startswith("__") and name.endswith("__")


def _is_class_object(value: Any) -> bool:
    """Return True when *value* is a class, tolerating context-bound proxies."""
    try:
        return isinstance(value, type)
    except Exception:
        return False


def _instance_class_name(value: Any) -> str:
    """Return the best class name for *value*, honoring transparent local proxies."""
    try:
        return value.__class__.__name__
    except Exception:
        return type(value).__name__


def _module_class_names(
    wrapped: types.ModuleType,
    mapping: dict[str, str],
    proxy_classes: frozenset[str],
) -> frozenset[str]:
    """Return class names whose module-level instances may receive ClassProxy."""
    class_names = set(proxy_classes)
    for python_attr in mapping.values():
        if "." in python_attr:
            continue
        try:
            value = getattr(wrapped, python_attr)
        except Exception:
            continue
        if _is_class_object(value):
            class_names.add(getattr(value, "__name__", python_attr))
    return frozenset(class_names)


# ---------------------------------------------------------------------------
# ClassProxy
# ---------------------------------------------------------------------------


class ClassProxy:
    """Wrap an object instance and expose curated Arabic attribute names.

    ``ClassProxy`` is deliberately small: explicit Arabic names are translated
    through the ``attributes`` table, and everything else falls through to the
    wrapped object. Common runtime protocols are forwarded so the proxy behaves
    like the original object in normal use.
    """

    __slots__ = ("_wrapped", "_attributes")

    def __init__(self, obj: Any, attributes: types.MappingProxyType | dict[str, str]) -> None:
        object.__setattr__(self, "_wrapped", obj)
        object.__setattr__(self, "_attributes", types.MappingProxyType(dict(attributes)))

    def _resolve_attr_name(self, name: str) -> str:
        if _is_dunder(name):
            return name
        attributes: types.MappingProxyType[str, str] = object.__getattribute__(self, "_attributes")
        return attributes.get(name, name)

    @staticmethod
    def _unwrap_other(other: Any) -> Any:
        if type(other) is ClassProxy:
            return object.__getattribute__(other, "_wrapped")
        return other

    def __getattr__(self, name: str) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return getattr(obj, self._resolve_attr_name(name))

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ClassProxy.__slots__:
            object.__setattr__(self, name, value)
            return
        obj: Any = object.__getattribute__(self, "_wrapped")
        setattr(obj, self._resolve_attr_name(name), value)

    def __delattr__(self, name: str) -> None:
        if name in ClassProxy.__slots__:
            object.__delattr__(self, name)
            return
        obj: Any = object.__getattribute__(self, "_wrapped")
        delattr(obj, self._resolve_attr_name(name))

    def __dir__(self) -> list[str]:
        obj: Any = object.__getattribute__(self, "_wrapped")
        attributes: types.MappingProxyType[str, str] = object.__getattribute__(self, "_attributes")
        return sorted(set(attributes.keys()) | set(dir(obj)))

    def __repr__(self) -> str:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return repr(obj)

    def __str__(self) -> str:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return str(obj)

    def __bool__(self) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return bool(obj)

    def __len__(self) -> int:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return len(obj)

    def __iter__(self) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return iter(obj)

    def __next__(self) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return next(obj)

    def __contains__(self, item: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return item in obj

    def __getitem__(self, key: Any) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        obj: Any = object.__getattribute__(self, "_wrapped")
        obj[key] = value

    def __delitem__(self, key: Any) -> None:
        obj: Any = object.__getattribute__(self, "_wrapped")
        del obj[key]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj(*args, **kwargs)

    def __eq__(self, other: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj == self._unwrap_other(other)

    def __ne__(self, other: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj != self._unwrap_other(other)

    def __lt__(self, other: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj < self._unwrap_other(other)

    def __le__(self, other: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj <= self._unwrap_other(other)

    def __gt__(self, other: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj > self._unwrap_other(other)

    def __ge__(self, other: Any) -> bool:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj >= self._unwrap_other(other)

    def __hash__(self) -> int:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return hash(obj)

    def __reduce_ex__(self, protocol: int) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj.__reduce_ex__(protocol)

    @property
    def __class__(self):  # type: ignore[override]
        """Return the wrapped object's class so ``isinstance`` stays transparent."""
        obj: Any = object.__getattribute__(self, "_wrapped")
        return obj.__class__


# ---------------------------------------------------------------------------
# InstanceProxy
# ---------------------------------------------------------------------------


class InstanceProxy:
    """Wraps a live Python object instance with an Arabic→Python name mapping.

    Only resolves entries of the form ``"ClassName.method"`` where
    *ClassName* matches the actual class of the wrapped instance. This
    prevents module-level entries (e.g. ``"جلسه" → "session"``) from
    accidentally being looked up on the wrong object.

    Calling ``تطبيق.طريق('/')`` (where ``تطبيق`` is a proxied Flask app):
      1. Looks up ``"طريق"`` in the mapping → ``"Flask.route"``
      2. Sees ``"Flask."`` prefix matches ``type(app).__name__ == "Flask"``
      3. Returns ``getattr(app, "route")`` — the bound method

    English names (e.g. ``.config``, ``.logger``) pass through unchanged.
    """

    __slots__ = ("_wrapped", "_mapping", "_proxy_classes")

    def __init__(
        self,
        obj: Any,
        mapping: types.MappingProxyType,
        proxy_classes: frozenset,
    ) -> None:
        object.__setattr__(self, "_wrapped", obj)
        object.__setattr__(self, "_mapping", mapping)
        object.__setattr__(self, "_proxy_classes", proxy_classes)

    def __getattr__(self, name: str) -> Any:
        obj: Any = object.__getattribute__(self, "_wrapped")
        mapping: types.MappingProxyType = object.__getattribute__(self, "_mapping")
        proxy_classes: frozenset = object.__getattribute__(self, "_proxy_classes")

        class_name = type(obj).__name__  # e.g. "Flask"
        prefix = class_name + "."

        if name in mapping:
            python_value: str = mapping[name]
            # Only handle entries prefixed with this instance's class name
            if python_value.startswith(prefix):
                method_name = python_value[len(prefix) :]  # e.g. "route"
                result = getattr(obj, method_name)
                # If the result is itself a proxy class, wrap it too
                if isinstance(result, type) and python_value in proxy_classes:
                    return ClassFactory(result, mapping, proxy_classes=proxy_classes)
                return result
            # Entry exists but is for a different class or is module-level;
            # fall through to English passthrough below.

        # English passthrough — works for unmapped English names
        if not _is_arabic_looking(name):
            return getattr(obj, name)

        # Unmapped Arabic name: warn and raise
        warnings.warn(
            f"'{name}' is not in the curated instance mapping for "
            f"'{class_name}'. "
            f"Use dir(...) to list available Arabic names.",
            DeprecationWarning,
            stacklevel=2,
        )
        raise AttributeError(
            f"'{class_name}' proxy has no Arabic attribute '{name}'. "
            f"Use dir(...) to list available Arabic names."
        )

    def __repr__(self) -> str:
        obj: Any = object.__getattribute__(self, "_wrapped")
        return f"<arabic-instance-proxy of {type(obj).__name__}>"

    def __dir__(self) -> list[str]:
        obj: Any = object.__getattribute__(self, "_wrapped")
        mapping: types.MappingProxyType = object.__getattribute__(self, "_mapping")
        class_name = type(obj).__name__
        prefix = class_name + "."
        instance_arabic = [k for k, v in mapping.items() if v.startswith(prefix)]
        english_pass = [n for n in dir(obj) if not _is_arabic_looking(n)]
        return sorted(set(instance_arabic + english_pass))


# ---------------------------------------------------------------------------
# ClassFactory
# ---------------------------------------------------------------------------


class ClassFactory:
    """Wraps a Python class so that calling it returns an InstanceProxy.

    When ``فلاسك.فلاسك`` is accessed on a ModuleProxy, it returns a
    ClassFactory wrapping ``flask.Flask``. Calling the factory
    (``فلاسك.فلاسك(__name__)``) creates a real Flask app and wraps it in
    an InstanceProxy, enabling Arabic method access on the result.
    """

    __slots__ = ("_cls", "_mapping", "_proxy_classes")

    def __init__(
        self,
        cls: type,
        mapping: types.MappingProxyType,
        *,
        proxy_classes: frozenset,
    ) -> None:
        object.__setattr__(self, "_cls", cls)
        object.__setattr__(self, "_mapping", mapping)
        object.__setattr__(self, "_proxy_classes", proxy_classes)

    def __call__(self, *args: Any, **kwargs: Any) -> InstanceProxy:
        cls: type = object.__getattribute__(self, "_cls")
        mapping: types.MappingProxyType = object.__getattribute__(self, "_mapping")
        proxy_classes: frozenset = object.__getattribute__(self, "_proxy_classes")
        instance = cls(*args, **kwargs)
        return InstanceProxy(instance, mapping, proxy_classes)

    def __repr__(self) -> str:
        cls: type = object.__getattribute__(self, "_cls")
        return f"<arabic-class-factory for {cls.__name__}>"

    @property
    def __class__(self):  # type: ignore[override]
        """Return the wrapped class so isinstance checks work."""
        return object.__getattribute__(self, "_cls")


# ---------------------------------------------------------------------------
# ModuleProxy
# ---------------------------------------------------------------------------


class ModuleProxy:
    """Transparent wrapper around a Python module with an Arabic→Python name mapping.

    Created by AliasFinder; not intended for direct instantiation by user code.

    Invariants
    ----------
    - ``self._wrapped`` is the underlying Python module object.
    - ``self._mapping`` is an immutable dict of Arabic → Python attribute names.
    - Attribute lookup first checks ``self._mapping``; on a hit it forwards to
      ``getattr(self._wrapped, mapping[name])`` (dotted paths resolved left-to-right).
    - If the resolved name is in ``self._proxy_classes``, a :class:`ClassFactory`
      is returned so that instantiation yields an :class:`InstanceProxy`.
    - An unmapped *Arabic* name emits DeprecationWarning then raises AttributeError
      with guidance text.
    - An unmapped *ASCII* name falls through to the wrapped module unchanged.

    Examples
    --------
    >>> import sys
    >>> proxy = ModuleProxy(sys, {"وسائط": "argv"}, arabic_name="نظام", proxy_classes=frozenset())
    >>> proxy.وسائط is sys.argv
    True
    >>> proxy.argv is sys.argv     # English fallthrough
    True
    """

    def __init__(
        self,
        wrapped: types.ModuleType,
        mapping: dict[str, str],
        *,
        attributes: dict[str, str] | None = None,
        arabic_name: str,
        proxy_classes: frozenset[str] = frozenset(),
    ) -> None:
        object.__setattr__(self, "_wrapped", wrapped)
        object.__setattr__(self, "_mapping", types.MappingProxyType(dict(mapping)))
        object.__setattr__(self, "_attributes", types.MappingProxyType(dict(attributes or {})))
        object.__setattr__(self, "_arabic_name", arabic_name)
        object.__setattr__(self, "_proxy_classes", proxy_classes)
        object.__setattr__(
            self,
            "_class_proxy_classes",
            _module_class_names(wrapped, mapping, proxy_classes),
        )

    # ------------------------------------------------------------------
    # Attribute access
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        mapping: types.MappingProxyType[str, str] = object.__getattribute__(self, "_mapping")
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        arabic_name: str = object.__getattribute__(self, "_arabic_name")
        proxy_classes: frozenset[str] = object.__getattribute__(self, "_proxy_classes")
        class_proxy_classes: frozenset[str] = object.__getattribute__(self, "_class_proxy_classes")
        attributes: types.MappingProxyType[str, str] = object.__getattribute__(self, "_attributes")

        if name in mapping:
            python_attr = mapping[name]
            # Support dotted paths such as "adapters.HTTPAdapter" or "Flask.route"
            if "." in python_attr:
                import importlib

                result: Any = wrapped
                for part in python_attr.split("."):
                    try:
                        result = getattr(result, part)
                    except AttributeError:
                        if isinstance(result, types.ModuleType):
                            importlib.import_module(f"{result.__name__}.{part}")
                            result = getattr(result, part)
                        else:
                            raise
            else:
                result = getattr(wrapped, python_attr)

            # If this is a proxy class, wrap it in a ClassFactory
            if (
                _is_class_object(result)
                and getattr(result, "__name__", python_attr) in proxy_classes
            ):
                return ClassFactory(result, mapping, proxy_classes=proxy_classes)

            if attributes and _instance_class_name(result) in class_proxy_classes:
                return ClassProxy(result, attributes)

            return result

        if _is_arabic_looking(name):
            warnings.warn(
                f"'{name}' is not in the curated mapping for '{arabic_name}'. "
                f"Use dir({arabic_name}) to list available Arabic names.",
                DeprecationWarning,
                stacklevel=2,
            )
            raise AttributeError(
                f"'{arabic_name}' has no attribute '{name}'. "
                f"'{name}' is not in the curated mapping. "
                f"Use dir({arabic_name}) to list available Arabic names."
            )

        # ASCII / non-Arabic name: forward unchanged to the wrapped module
        return getattr(wrapped, name)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def __dir__(self) -> list[str]:
        """Return Arabic names from the mapping *plus* English names from the wrapped module."""
        mapping: types.MappingProxyType[str, str] = object.__getattribute__(self, "_mapping")
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        return sorted(set(list(mapping.keys()) + dir(wrapped)))

    def __repr__(self) -> str:
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        arabic_name: str = object.__getattribute__(self, "_arabic_name")
        return f"<arabic-proxy of {wrapped.__name__} via {arabic_name}>"

    # ------------------------------------------------------------------
    # isinstance / type reflexivity
    # ------------------------------------------------------------------

    @property
    def __class__(self):  # type: ignore[override]
        """Return the wrapped module's class so ``isinstance(proxy, ModuleType)`` works."""
        wrapped: types.ModuleType = object.__getattribute__(self, "_wrapped")
        return wrapped.__class__
