# coding=utf-8
# Copyright 2024 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility functions for huggingface_dataset_builder."""

from typing import Type

import immutabledict
import numpy as np
from tensorflow_datasets.core.utils.lazy_imports_utils import tensorflow as tf


_HF_DTYPE_TO_NP_DTYPE = immutabledict.immutabledict({
    'bool': np.bool_,
    'float': np.float32,
    'double': np.float64,
    'large_string': np.object_,
    'utf8': np.object_,
    'string': np.object_,
})


def convert_to_np_dtype(hf_dtype: str) -> Type[np.generic]:
  """Returns the `np.dtype` scalar feature.

  Args:
    hf_dtype: Huggingface dtype.

  Raises:
    ValueError: If couldn't recognize Huggingface dtype.
  """
  if np_dtype := _HF_DTYPE_TO_NP_DTYPE.get(hf_dtype):
    return np_dtype
  elif hasattr(np, hf_dtype):
    return getattr(np, hf_dtype)
  if hf_dtype.startswith('timestamp'):
    # Timestamps are converted to seconds since UNIX epoch.
    return np.int64
  elif hasattr(tf.dtypes, hf_dtype):
    return getattr(tf.dtypes, hf_dtype)
  else:
    raise ValueError(
        f'Unrecognized type {hf_dtype}. Please open an issue if you think '
        'this is a bug.'
    )


def convert_hf_dataset_name(hf_dataset_name: str) -> str:
  """Converts Huggingface dataset name to a TFDS compatible dataset name.

  Huggingface dataset names can contain characters that are not supported in
  TFDS. For example, in Huggingface a dataset name like `a/b` is supported,
  while in TFDS `b` would be parsed as the config.

  Examples:
  - `hf_dataset_name='codeparrot/github-code'` becomes
  `codeparrot__github_code`.

  Args:
    hf_dataset_name: Huggingface dataset name.

  Returns:
    The TFDS compatible dataset name.
  """
  return (
      hf_dataset_name.replace('-', '_')
      .replace('.', '_')
      .replace('/', '__')
      .lower()
  )


def convert_hf_config_name(hf_config_name: str | None) -> str | None:
  """Converts Huggingface config name to a TFDS compatible config name.

  Args:
    hf_config_name: Optional Huggingface config name.

  Returns:
    The TFDS compatible config name.
  """
  if hf_config_name is None:
    return hf_config_name
  return hf_config_name.lower().replace(',', '_')