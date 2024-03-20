from pylie import SO3, SE3, SE23 
import numpy as np


def SO3LeftJacobian(arr: np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (3, 1):
        raise ValueError

    angle = np.linalg.norm(arr)

    # Near |phi|==0, use first order Taylor expansion
    if np.isclose(angle, 0.):
        return np.eye(3) + 0.5 * SO3.wedge(arr)

    axis = arr / angle
    s = np.sin(angle)
    c = np.cos(angle)

    return (s / angle) * np.eye(3) + \
           (1 - s / angle) * np.outer(axis, axis) + \
           ((1 - c) / angle) * SO3.wedge(axis)


def SO3RightJacobian(arr : np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (3, 1):
        raise ValueError

    angle = np.linalg.norm(arr)

    # Near |phi|==0, use first order Taylor expansion
    if np.isclose(angle, 0.):
        return np.eye(3) - 0.5 * SO3.wedge(arr)

    axis = arr / angle
    s = np.sin(angle)
    c = np.cos(angle)

    # This is the right Jacobian
    J = np.eye(3) - ((1 - c)/angle) * SO3.wedge(axis) + ((angle - s)/angle) * (SO3.wedge(axis) @ SO3.wedge(axis))

    return J

def SO3_PT(arr : np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (3, 1):
        raise ValueError
    
    Pt = SO3.exp(-0.5*arr)

    return Pt.as_matrix()

def SO3_PT_CURV(arr : np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (3, 1):
        raise ValueError
    arr_ad = SO3.wedge(arr)
    Pt = SO3.exp(-0.5*arr)
    curv = np.eye(3) + (1/24) * arr_ad @ arr_ad

    return (Pt @ curv)


def SE3LeftJacobianQ(arr: np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (6, 1):
        raise ValueError

    phi = arr[0:3, 0:1]  # rotation part
    rho = arr[3:6, 0:1]  # translation part

    rx = SO3.wedge(rho)
    px = SO3.wedge(phi)

    ph = np.linalg.norm(phi)
    ph2 = ph * ph
    ph3 = ph2 * ph
    ph4 = ph3 * ph
    ph5 = ph4 * ph

    cph = np.cos(ph)
    sph = np.sin(ph)

    m1 = 0.5
    m2 = (ph - sph) / ph3
    m3 = (0.5 * ph2 + cph - 1.) / ph4
    m4 = (ph - 1.5 * sph + 0.5 * ph * cph) / ph5

    t1 = rx
    t2 = px @ rx + rx @ px + px @ rx @ px
    t3 = px @ px @ rx + rx @ px @ px - 3. * px @ rx @ px
    t4 = px @ rx @ px @ px + px @ px @ rx @ px

    return m1 * t1 + m2 * t2 + m3 * t3 + m4 * t4


def SE3LeftJacobian(arr: np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (6, 1):
        raise ValueError

    phi = arr[0:3, 0:1]  # rotation part
    # rho = arr[3:6, 0:1]  # translation part

    # Near |phi|==0, use first order Taylor expansion
    if np.isclose(np.linalg.norm(phi), 0.):
        return np.eye(6) + 0.5 * SE3.adjoint(arr)

    SO3_JL = SO3LeftJacobian(phi)
    QL = SE3LeftJacobianQ(arr)

    J = np.zeros([6, 6])
    J[0:3, 0:3] = SO3_JL
    J[0:3, 3:6] = QL
    J[3:6, 3:6] = SO3_JL

    return J

def SE3RightJacobian(arr: np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (6, 1):
        raise ValueError

    phi = arr[0:3, 0:1]

    # Near |phi|==0, use first order Taylor expansion
    if np.isclose(np.linalg.norm(phi), 0.):
        return np.eye(6) - 0.5 * SE3.adjoint(arr)
    
    SO3_JR = SO3RightJacobian(phi)
    QR = SE3LeftJacobianQ(-arr)

    J = np.zeros([6, 6])
    J[0:3, 0:3] = SO3_JR
    J[0:3, 3:6] = QR
    J[3:6, 3:6] = SO3_JR

    return J


def SE23LeftJacobian(arr: np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (9, 1):
        raise ValueError

    phi = arr[0:3, 0:1]  # rotation part
    rho = arr[3:6, 0:1]  # translation part 1
    psi = arr[6:9, 0:1]  # translation part 2

    # Near |phi|==0, use first order Taylor expansion
    if np.isclose(np.linalg.norm(phi), 0.):
        return np.eye(9) + 0.5 * SE23.adjoint(arr)

    SO3_JL = SO3LeftJacobian(phi)
    QL1 = SE3LeftJacobianQ(np.vstack((phi, rho)))
    QL2 = SE3LeftJacobianQ(np.vstack((phi, psi)))

    J = np.zeros([9, 9])
    J[0:3, 0:3] = SO3_JL
    J[3:6, 3:6] = SO3_JL
    J[6:9, 6:9] = SO3_JL
    J[0:3, 3:6] = QL1
    J[0:3, 6:9] = QL2

    return J

def SE23RightJacobian(arr: np.ndarray) -> np.ndarray:
    if not isinstance(arr, np.ndarray):
        raise TypeError
    elif not arr.shape == (9, 1):
        raise ValueError

    phi = arr[0:3, 0:1]  # rotation part
    rho = arr[3:6, 0:1]  # translation part 1
    psi = arr[6:9, 0:1]  # translation part 2

    # Near |phi|==0, use first order Taylor expansion
    if np.isclose(np.linalg.norm(phi), 0.):
        return np.eye(9) - 0.5 * SE23.adjoint(arr)

    SO3_JR = SO3RightJacobian(phi)
    QR1 = SE3LeftJacobianQ(-np.vstack((phi, rho)))
    QR2 = SE3LeftJacobianQ(-np.vstack((phi, psi)))

    J = np.zeros([9, 9])
    J[0:3, 0:3] = SO3_JR
    J[3:6, 3:6] = SO3_JR
    J[6:9, 6:9] = SO3_JR
    J[0:3, 3:6] = QR1
    J[0:3, 6:9] = QR2

    return J