# AoD

### 1. XOR's problem
+ Install PyBrain, following this [article](https://stackoverflow.com/questions/28896314/no-module-named-structure-when-installing-pybrain-even-though-its-in-the-fold)
+ Fix problem with expm2 in scipy.linalg, following this [issue](https://github.com/pybrain/pybrain/issues/228)
```python
    # functions.py
    - from scipy.linalg import inv, det, svd, logm, expm2
    + from scipy.linalg import inv, det, svd, logm, expm
```
+ Learn how to save object by using Pickle, following this [article](https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence)

```python
    ...
    print(net.activate((0, 0)))     # [-5.55111512e-17]
```