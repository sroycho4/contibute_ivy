import ivy
from .generic import NDFrame


class Series(NDFrame):
    def __init__(
        self,
        data,
        index=None,
        dtype=None,
        name=None,
        copy=False,
        fastpath=False,
        columns=None,
        *args,
        **kwargs,
    ):
        super().__init__(
            data,
            index,
            columns=None,
            dtype=dtype,
            name=name,
            copy=copy,
            *args,
            **kwargs,
        )
        assert self.array.ndim == 1, "Series Data must be 1-dimensional"

    def __repr__(self):
        series_name = f"{self.name} " if self.name is not None else ""
        return (
            f"frontends.pandas.Series {series_name}({self.array.to_list()},"
            f" index={self.index.array.to_list()})"
        )

    def __getitem__(self, index_val):
        if isinstance(index_val, slice):
            return Series(
                self.array[index_val],
                index=self.index[index_val],
                name=self.name,
                dtype=self.dtype,
                copy=self.copy,
            )
        return self.array[self.index.index(index_val)].item()

    def __getattr__(self, item):
        if item in self.index:
            return self[item]
        else:
            return super().__getattr__(item)

    def __len__(self):
        return len(self.array)

    def sum(self, axis=None, skipna=True, numeric_only=False, min_count=0, **kwargs):
        _array = self.array
        if min_count > 0:
            if ivy.has_nans(_array):
                number_values = _array.size - ivy.sum(ivy.isnan(_array))
            else:
                number_values = _array.size
            if min_count > number_values:
                return ivy.nan
        if skipna:
            return ivy.nansum(_array)
        return _array.sum()

    def mean(self, axis=None, skipna=True, numeric_only=False, **kwargs):
        if skipna:
            return ivy.nanmean(self.array)
        return self.array.mean()

    def add(self, other, level=None, fill_value=None, axis=0):
        # todo add level (with multiindex) and fill_value (with wrapper)
        # todo handle data alignment
        new_array = ivy.add(self.array, other.array)
        return Series(new_array)

    def get(self, key, default=None):
        if key in self.index:
            return self[key]
        return default

    def keys(self):
        return self.index
