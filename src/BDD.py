import collections
from typing import Tuple, List, Dict
from pyeda.inter import *      # BinaryDecisionDiagram, bddvar, expr, expr2bdd
from .PetriNet import PetriNet
import numpy as np

# Hằng BDD True/False
BDD_TRUE = expr2bdd(expr(1))
BDD_FALSE = expr2bdd(expr(0))


def _transition_bdd(
    I_row: np.ndarray,
    O_row: np.ndarray,
    p: List[BinaryDecisionDiagram],
    q: List[BinaryDecisionDiagram],
) -> BinaryDecisionDiagram:
    """
    BDD cho một transition với semantics 1-safe "strict".

    Giả sử net 1-safe (mỗi place chứa 0/1 token) và ta ENCODE thẳng cả 1-safe
    vào precondition:

      Precondition (trên p):
        - Nếu I[i] == 1         : place i phải có token  (p[i] = 1)
        - Nếu I[i] == 0, O[i]==1: place i phải rỗng      (p[i] = 0)
          (không được tạo token lên place đang có token)

      Effect (liên hệ giữa p và q):
        - I=1, O=0 : q[i] = 0        (consume)
        - I=0, O=1 : q[i] = 1        (produce)
        - I=1, O=1 : q[i] = 1, p[i]=1 (giữ token, nhưng pre đã yêu cầu p[i]=1)
        - I=0, O=0 : q[i] == p[i]    (unchanged)
    """
    n = len(p)

    pre = BDD_TRUE
    eff = BDD_TRUE

    for i in range(n):
        inp = int(I_row[i])
        out = int(O_row[i])

        # --------- PRECONDITION (p) ----------
        if inp == 1:
            # cần token ở input place
            pre &= p[i]
        elif out == 1:
            # 1-safe strict: place nhận token PHẢI đang rỗng
            pre &= ~p[i]

        # --------- EFFECT (q so với p) ----------
        if inp == 1 and out == 0:
            # token bị tiêu thụ
            eff &= ~q[i]
        elif inp == 0 and out == 1:
            # token được tạo
            eff &= q[i]
        else:
            # không đổi hoặc I=1,O=1: q[i] == p[i]
            eff &= ((q[i] & p[i]) | (~q[i] & ~p[i]))

    return pre & eff


def _exists(bdd: BinaryDecisionDiagram,
            vars_: List[BinaryDecisionDiagram]) -> BinaryDecisionDiagram:
    """
    ∃ vars_. bdd  bằng smoothing lần lượt từng biến.
    """
    res = bdd
    for v in vars_:
        res = res.smoothing(v)
    return res


def count_boolean_markings(R, place_ids):
    len_places = len(place_ids)
    sum = 0
    for sat in R.satisfy_all():
        print (sat)
        sum += 2**(len_places - len(sat))
    return sum


def bdd_reachable(pn: PetriNet) -> Tuple[BinaryDecisionDiagram, int]:
    """
    Symbolic reachability cho 1-safe Petri net bằng BDD.

    Biến:
      - p[i] : trạng thái hiện tại (place i có token?)
      - q[i] : trạng thái kế tiếp

    Transition relation:
      T(p, q) = OR_t T_t(p, q)

    Reachable set R(p) qua fixpoint:
      R0(p)      = encoding(M0)
      Post(R)(q) = ∃p. (R(p) ∧ T(p, q))
      R_{k+1}(p) = R_k(p) ∨ Post(R)(p)   (sau khi rename q→p)

    Lặp đến khi R_{k+1} ≡ R_k.
    """
    # -----------------------------
    # Lấy dữ liệu từ PetriNet
    # -----------------------------
    P_ids = pn.place_names
    I = np.array(pn.I, dtype=int)   # (num_trans, num_places)
    O = np.array(pn.O, dtype=int)
    M0 = np.array(pn.M0, dtype=int) # (num_places,)

    n_places = len(P_ids)
    n_trans  = I.shape[0]

    # -----------------------------
    # Tạo biến BDD cho p (hiện tại) và q (kế tiếp)
    # -----------------------------
    p_vars: List[BinaryDecisionDiagram] = [bddvar(pid) for pid in P_ids]
    q_vars: List[BinaryDecisionDiagram] = [bddvar(pid + "'") for pid in P_ids]

    # -----------------------------
    # Global transition relation T(p, q)
    # -----------------------------
    T = BDD_FALSE
    for t in range(n_trans):
        T_t = _transition_bdd(I[t, :], O[t, :], p_vars, q_vars)
        T |= T_t

    # -----------------------------
    # Encode initial marking M0 vào BDD R(p)
    # -----------------------------
    R = BDD_TRUE
    for i in range(n_places):
        if M0[i] == 1:
            R &= p_vars[i]
        else:
            R &= ~p_vars[i]

    # -----------------------------
    # Fixpoint iteration:
    #   R_{k+1} = R_k ∨ Post(R_k)
    # -----------------------------
    # iter_no = 0
    while True:
        # iter_no += 1
        # print("\n======================")
        # print(f" ITERATION {iter_no}")

        # step(p, q) = R(p) ∧ T(p, q)
        step = R & T
        # print("\n[STEP  BDD → EXPR]")
        # print(bdd2expr(step))

        # Post(R)(q) = ∃p. step(p, q)
        post_q = _exists(step, p_vars)
        # print("\n[POST_Q  BDD → EXPR]")
        # print(bdd2expr(post_q))

        # Đổi tên q -> p để nhập về không gian trạng thái p
        rename_map = {q_vars[i]: p_vars[i] for i in range(n_places)}
        post_p = post_q.compose(rename_map)
        # print("\n[POST_P (renamed)  BDD → EXPR]")
        # print(bdd2expr(post_p))

        # R_new = R ∪ post_p
        R_new = R | post_p
        # print("\n[R_NEW  BDD → EXPR]")
        # print(bdd2expr(R_new))

        # STOP if fixpoint
        if R_new.equivalent(R):
            # print("\n>>> FIXPOINT REACHED <<<")
            break

        R = R_new


    # Số marking reachable = số nghiệm 0/1 của R
    count = count_boolean_markings(R, P_ids)

    return R, count
