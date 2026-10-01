"""Tests for room.py. They drive whole sessions with fake sub-agents (no model calls), and check the
dealer, the routing, the deterministic checks, the ship gates and the file formats.

    python3 -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SKILL = os.path.join(REPO, "skills", "marketing-room")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import room  # noqa: E402

B2B = os.path.join(REPO, "examples", "brief-b2b-saas-leadgen.md")
AUDIT = os.path.join(REPO, "examples", "brief-ecom-audit.md")
CSVS = [os.path.join(REPO, "examples", "sample-google-export.csv"),
        os.path.join(REPO, "examples", "sample-meta-export.csv")]


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = room.main([str(a) for a in argv])
    return code, buf.getvalue()


def load(d):
    with open(os.path.join(d, "room.json"), encoding="utf-8") as fh:
        return json.load(fh)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def outs(job):
    return dict(zip(room.OUTPUTS[job["kind"]], job["outputs"]))


LOREM = ("We run this channel against the brief's KPIs with a clear structure, named owners and dated "
         "hand-offs. The plan ties every line to a requirement and says what it needs from the other seats. ")


class Fake:
    """Plays every role. The knobs make it misbehave in the ways the tests need."""

    def __init__(self, over_budget=False, concede=True, hollow=False, resolve_accept=True, reviews=None,
                 blocking_question=False, cast=None, bad_json_once=(), bad_json_always=(), drop_tag_v1=None,
                 final_over_budget=False):
        self.over_budget = over_budget
        self.concede = concede
        self.hollow = hollow
        self.resolve_accept = resolve_accept
        self.reviews = list(reviews or [])
        self.blocking_question = blocking_question
        self.cast = cast or ["google-ads", "linkedin-ads", "meta-ads", "ux", "developer", "creative-ops",
                             "copywriter"]
        self.bad_json_once = set(bad_json_once)
        self.bad_json_always = set(bad_json_always)
        self.drop_tag_v1 = drop_tag_v1
        self.final_over_budget = final_over_budget
        self.calls = 0
        self.seen = set()

    def do(self, state, job):
        self.calls += 1
        jid = job["id"]
        if jid in self.bad_json_always or (jid in self.bad_json_once and jid not in self.seen):
            self.seen.add(jid)
            for p in job["outputs"]:
                write(p, "this is not json and the proposal is short")
            return
        getattr(self, job["kind"])(state, job, outs(job))

    # -- the Project Head, opening
    def intake(self, state, job, o):
        brief = room.read_brief(state)
        lines = [l.strip("-* ").strip() for l in brief.splitlines()
                 if l.strip() and not l.startswith("#") and len(l.split()) > 8]
        reqs = []
        for i, l in enumerate(lines[:6]):
            reqs.append({"text": "requirement %d" % (i + 1), "quote": " ".join(l.split()[:7]), "must": i < 4})
        qs = [{"q": "Is November a ramp month?", "why": "targets", "blocking": self.blocking_question,
               "default": "November is a ramp month at 70% of target"}]
        data = {
            "task_type": "campaign", "deliverable": "an integrated 90-day plan",
            "facts": {"budget_total": 60000, "currency": "USD", "budget_period": "month",
                      "flight_start": "2026-11-02", "flight_end": "2027-01-29", "today": "2026-10-01",
                      "geo": ["US", "UK"],
                      "kpis": [{"metric": "MQLs", "target": 400, "unit": "per month", "direction": "min"},
                               {"metric": "CPL", "target": 150, "unit": "USD", "direction": "max"}],
                      "tracking": {"conversion_events": True, "capi_or_enhanced": False, "consent_mode": False}},
            "requirements": reqs,
            "cast": [{"seat": s, "priority": i + 1, "why": "needed", "maybe": False, "trigger_quote": ""}
                     for i, s in enumerate(self.cast)],
            "questions": qs, "assumptions": [{"text": "MQL to SQL rate is 15%", "value": "15%"}]}
        write(o["json"], json.dumps(data))
        write(o["md"], "# Intake\n" + LOREM)

    # -- a seat's first proposal
    def sidecar(self, seat):
        ad = {"google-ads": ("google", 30000 if self.over_budget else 22000, {"cpc": 8, "cvr": 5}, 3),
              "linkedin-ads": ("linkedin", 30000 if self.over_budget else 22000, {"cpa": 110}, 3),
              "meta-ads": ("meta", 15000 if self.over_budget else 12000, {"cpm": 20, "ctr": 1, "cvr": 5}, 4)}
        own = room.roster()["ownership"]
        sc = {"owns": [{"key": k, "role": "A"} for k, v in own.items() if v == seat],
              "deliverables": ["the %s plan" % seat], "needs": [], "impacts": [], "kpis": [],
              "budget_ask": None, "forecast": [], "lead_times": [], "tracking_plan": None, "capacity": None,
              "risks": [{"risk": "it underdelivers", "likelihood": "M", "mitigation": "weekly review"}],
              "assumptions": []}
        if seat in ad:
            plat, amt, eff, units = ad[seat]
            sc["budget_ask"] = {"amount": amt, "currency": "USD", "period": "month", "source": "ASSUMPTION"}
            f = {"platform": plat, "budget": amt, "period": "month", "units": units, "unit_type": "campaign",
                 "optimization_event": "lead", "source": "ASSUMPTION"}
            f.update(eff)
            sc["forecast"] = [f]
            sc["needs"] = [{"from": "developer", "what": "landing page", "by": "2026-10-26", "blocking": True}]
            sc["impacts"] = [{"on": "creative-ops", "effect": "-", "note": "asset volume"}]
        if seat == "measurement":
            sc["tracking_plan"] = {"conversion_events": "exists", "capi_or_enhanced": "planned",
                                   "consent_mode": "planned", "ready_by": "2026-10-28"}
        if seat == "developer":
            sc["lead_times"] = [{"item": "landing page rebuild", "days": 15, "blocking": True}]
        if seat == "creative-ops":
            sc["capacity"] = {"assets_per_week": 12}
        return sc

    def kickoff(self, state, job, o):
        write(o["md"], "# %s\n" % job["seat"] + LOREM * 3)
        write(o["json"], json.dumps(self.sidecar(job["seat"])))

    def challenge(self, state, job, o):
        seat, rnd = job["seat"], job["round"]
        targets = state["targets"][str(rnd)][seat]
        chs = []
        for t in targets:
            chs.append({"to": t, "severity": "MAJOR", "kind": "CLASHES", "point": "%s's plan leaves %s short" % (
                t, seat), "lens_test": "the number that must hold", "evidence": "R1", "requirement_ids": ["R1"],
                "impact_on_me": "more work", "ask": "change it"})
        write(o["json"], json.dumps({"challenges": chs, "clean": []}))

    def _current_sidecar(self, state, seat):
        with open(state["seats"][seat]["json"], encoding="utf-8") as fh:
            return json.load(fh)

    def _fixed(self, sc):
        sc = json.loads(json.dumps(sc))
        if sc.get("budget_ask") and sc["budget_ask"].get("amount"):
            sc["budget_ask"]["amount"] = round(sc["budget_ask"]["amount"] * 0.75)
            for f in sc.get("forecast") or []:
                f["budget"] = sc["budget_ask"]["amount"]
                f["units"] = 1
        sc["assumptions"] = (sc.get("assumptions") or []) + [{"text": "revised after the debate %d" % self.calls}]
        return sc

    def respond(self, state, job, o):
        seat, rnd = job["seat"], job["round"]
        items = state["inboxes"][str(rnd)][seat]
        resp = []
        for k, iid in enumerate(items):
            if self.hollow:
                resp.append({"id": iid, "verdict": "CONCEDE", "reply": "fair", "changes": []})
            elif self.concede:
                resp.append({"id": iid, "verdict": "CONCEDE", "reply": "fair", "changes": ["cut the ask"]})
            else:
                resp.append({"id": iid.lower(), "verdict": "REBUT" if k % 2 == 0 else "COMPROMISE",
                             "reply": "no, because R1", "changes": []})
        sc = self._current_sidecar(state, seat)
        if self.concede and not self.hollow:
            sc = self._fixed(sc)
        prev = read(state["seats"][seat]["pov"])
        write(o["md"], prev if self.hollow or not self.concede else prev + "\nRevised. " + LOREM)
        write(o["json"], json.dumps({"responses": resp, "sidecar": sc}))

    def moderate(self, state, job, o):
        if job.get("remoderate"):
            cs = [{"id": cid, "title": "t", "items": [], "parties": state["conflicts"][cid]["parties"],
                   "proposal": "a better middle ground %d" % self.calls} for cid in job["existing"]]
        else:
            cs = []
            for iid in job["must_place"]:
                cs.append({"id": "", "title": "about %s" % iid, "items": [iid], "parties": [],
                           "trade_off": "speed against quality", "positions": {},
                           "proposal": "split the difference on %s" % iid, "client_decision": False})
        write(o["json"], json.dumps({"conflicts": cs, "summary": "ok"}))

    def resolve(self, state, job, o):
        seat, s = job["seat"], job["round"]
        mine = [c for c in state["resolve_set"] if seat in state["conflicts"][c]["parties"]]
        ans = [{"conflict": c, "verdict": "ACCEPT" if self.resolve_accept else "REJECT", "why": "fine",
                "counter": "" if self.resolve_accept else "do it my way"} for c in mine]
        sc = self._current_sidecar(state, seat)
        if self.resolve_accept:
            sc = self._fixed(sc)
        prev = read(state["seats"][seat]["pov"])
        write(o["md"], prev + ("\nAccepted. " if self.resolve_accept else ""))
        write(o["json"], json.dumps({"answers": ans, "sidecar": sc}))

    def ruling(self, state, job, o):
        rs = [{"conflict": c, "decision": "the Project Head splits %s" % c, "side": "split", "reason": "R1 first",
               "client_decision": False} for c in job["escalated"]]
        write(o["json"], json.dumps({"rulings": rs}))

    def integrate(self, state, job, o):
        tt = state["intake"]["task_type"]
        heads = room.outline_headings(tt)
        tags = [r["id"] for r in state["requirements"]]
        if job["round"] == 1 and self.drop_tag_v1:
            tags = [t for t in tags if t != self.drop_tag_v1]
        body = ["# Plan"]
        for i, h in enumerate(heads):
            body.append("## %s" % h)
            body.append(LOREM)
            if i == 0:
                body.append(" ".join("[%s]" % t for t in tags))
            if h.startswith("Decisions"):
                body.append(" ".join("[%s]" % dd for dd in state["decisions"]))
        write(o["md"], "\n\n".join(body))
        amt = 70000 if self.final_over_budget else 55000
        plan = {"budget": [{"line": "all media", "seat": "client-lead", "amount": amt, "currency": "USD",
                            "period": "month", "source": "D1"}],
                "raci": [{"key": "tracking-plan", "accountable": "measurement", "responsible": ["developer"],
                          "consulted": []}],
                "timeline": [{"milestone": "launch", "date": "2026-11-02", "owner": "client-lead"}],
                "client_questions": [{"q": "Approve the split?", "options": ["yes", "no"], "recommended": "yes"}]}
        write(o["json"], json.dumps(plan))

    def review(self, state, job, o):
        spec = self.reviews.pop(0) if self.reviews else ("SHIP", 8)
        verdict, score = spec
        reqs = [{"id": r["id"], "status": "met", "where": "Executive summary"} for r in state["requirements"]]
        data = {"requirements": reqs, "scores": {k: score for k, _w in room.WEIGHTS},
                "blockers": [] if score >= 5 else ["it is weak"],
                "required_changes": [{"change": "tighten it", "ref": "R1"}] if verdict == "REVISE" else [],
                "verdict": verdict, "client_questions": [], "summary": "It holds up."}
        write(o["json"], json.dumps(data))


def drive(d, fake, limit=300, solo=False):
    for _ in range(limit):
        st = load(d)
        if st["stage"] == "done":
            return st
        if st["stage"] == "gate":
            code, out = run("answer", "--dir", d, "--assume")
            assert code == 0, out
            continue
        if room.pending_jobs(st):
            code, out = run("prompts", "--dir", d, *(["--one"] if solo else []))
            assert code == 0, out
            st = load(d)
            todo = room.pending_jobs(st)[:1] if solo else room.pending_jobs(st)
            for j in todo:
                fake.do(st, j)
            if solo and room.pending_jobs(load(d)):
                continue
        code, out = run("collect", "--dir", d)
        assert code == 0, out
    raise AssertionError("the room did not finish")


class TempDir(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="room-test-")
        self.d = os.path.join(self.tmp, "run")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def init(self, *extra, brief=B2B):
        code, out = run("init", "--brief", brief, "--dir", self.d, "--seed", 7, "--today", "2026-10-01", *extra)
        self.assertEqual(code, 0, out)
        return out


# ---------------------------------------------------------------- whole sessions

class FullSessions(TempDir):
    def test_default_session_ships_with_every_file(self):
        self.init()
        fake = Fake()
        st = drive(self.d, fake)
        self.assertEqual(st["result"]["status"], "SHIPPED")
        self.assertIn("client-lead", st["cast"])
        self.assertIn("measurement", st["cast"])
        for name in ("deliverable.md", "report.md", "budget.csv", "raci.csv", "assumptions.csv",
                     "client-questions.md", "timeline.csv"):
            self.assertTrue(os.path.isfile(os.path.join(self.d, "final", name)), name)
        n = len(st["cast"])
        p = room.plan_numbers(n, 1, 2)
        self.assertGreaterEqual(fake.calls, p["min"])
        self.assertLessEqual(fake.calls, p["max"])

    def test_briefs_are_filled_and_share_one_client_brief(self):
        self.init()
        drive(self.d, Fake())
        brief = room.read_brief(load(self.d))
        briefs = os.listdir(os.path.join(self.d, "briefs"))
        self.assertGreater(len(briefs), 10)
        for name in briefs:
            text = read(os.path.join(self.d, "briefs", name))
            self.assertNotIn("{{", text, name)
            m = re.search(r"=== THE CLIENT BRIEF[^\n]*===\n(.*?)\n=== END OF THE BRIEF ===", text, re.S)
            self.assertIsNotNone(m, name)
            self.assertEqual(m.group(1), brief, name)

    def test_quick_session_is_small_and_has_no_resolve_rounds(self):
        self.init("--quick")
        st = drive(self.d, Fake(concede=False))
        self.assertLessEqual(len(st["cast"]), 5)
        self.assertFalse(any(j.startswith("s") for j in st["jobs"]))
        self.assertIn(st["result"]["status"], ("SHIPPED", "SHIPPED_WITH_CAVEATS"))
        if st["conflicts"]:
            self.assertTrue(any(j.startswith("r") for j in st["jobs"]), "escalations need a ruling")

    def test_deep_session_runs_two_challenge_rounds(self):
        self.init("--deep")
        st = drive(self.d, Fake(concede=False))
        self.assertTrue(any(j.startswith("c2.") for j in st["jobs"]))
        self.assertEqual(set(st["lenses"]), {"1", "2"})

    def test_all_seats(self):
        self.init("--all")
        st = drive(self.d, Fake())
        self.assertEqual(len(st["cast"]), len(room.seat_ids()))

    def test_exact_seats_add_no_rule_seats(self):
        self.init("--seats", "google-ads,seo,ux")
        st = drive(self.d, Fake())
        self.assertEqual(st["cast"], ["google-ads", "seo", "ux"])

    def test_nothing_is_written_outside_the_run_folder(self):
        self.init()
        drive(self.d, Fake())
        self.assertEqual(os.listdir(self.tmp), ["run"])

    def test_solo_mode_writes_one_brief_at_a_time(self):
        self.init("--solo")
        st = load(self.d)
        self.assertEqual(st["profile"], "quick")
        run("collect", "--dir", self.d)  # nothing to collect yet: must refuse, not crash
        fake = Fake()
        code, out = run("prompts", "--dir", self.d, "--one")
        self.assertEqual(len(os.listdir(os.path.join(self.d, "briefs"))), 1)
        st = drive(self.d, fake, solo=True)
        self.assertEqual(st["result"]["status"], "SHIPPED")
        report = read(os.path.join(self.d, "final", "report.md"))
        self.assertIn("independence is structural only", report)


class Debate(TempDir):
    def test_over_budget_is_a_system_blocker_that_the_parties_fix(self):
        self.init()
        st = drive(self.d, Fake(over_budget=True, concede=False))
        blocker = [c for c in st["conflicts"].values() if "S-BUDGET-OVER" in c["items"]]
        self.assertEqual(len(blocker), 1)
        self.assertEqual(blocker[0]["severity"], "BLOCKER")
        self.assertEqual(blocker[0]["status"], "resolved")
        self.assertNotIn("S-BUDGET-OVER", st["checks"])

    def test_rejections_escalate_to_a_ruling(self):
        self.init()
        st = drive(self.d, Fake(over_budget=True, concede=False, resolve_accept=False))
        self.assertTrue(any(j.startswith("r") and st["jobs"][j]["kind"] == "ruling" for j in st["jobs"]))
        ruled = [c for c in st["conflicts"].values() if c["status"] == "ruled"]
        self.assertTrue(ruled)
        self.assertTrue(all(st["decisions"][c["decision"]]["by"] == "the Project Head" for c in ruled))
        # no progress in the first resolve round means no second resolve round
        self.assertFalse(any(j.startswith("s2.") for j in st["jobs"]))

    def test_hollow_concessions_stay_contested(self):
        self.init()
        st = drive(self.d, Fake(hollow=True))
        hollow = [c for c in st["challenges"].values() if c["hollow"]]
        self.assertTrue(hollow)
        self.assertTrue(all(c.get("conflict") for c in hollow if c["severity"] != "MINOR"))

    def test_real_concessions_close_challenges(self):
        self.init()
        st = drive(self.d, Fake(concede=True))
        closed = [c for c in st["challenges"].values() if c["status"] == "closed"]
        self.assertEqual(len(closed), len(st["challenges"]))

    def test_meta_learning_phase_check_fires_then_clears(self):
        self.init()
        fake = Fake(concede=True)
        # run just past kickoff
        for _ in range(20):
            st = load(self.d)
            if st["stage"] == "challenge":
                break
            run("prompts", "--dir", self.d)
            st = load(self.d)
            for j in room.pending_jobs(st):
                fake.do(st, j)
            run("collect", "--dir", self.d)
        st = load(self.d)
        self.assertIn("S-LEARN-meta-ads-meta", st["checks"])
        self.assertNotIn("S-TRACK-CONSENT", st["checks"])  # measurement plans consent mode before launch
        st = drive(self.d, fake)
        self.assertNotIn("S-LEARN-meta-ads-meta", st["checks"])
        self.assertIn("S-LEARN-meta-ads-meta", st["checks_cleared"])


class Gates(TempDir):
    def test_revise_then_ship(self):
        self.init()
        st = drive(self.d, Fake(reviews=[("REVISE", 6), ("SHIP", 8)]))
        self.assertEqual(st["result"]["status"], "SHIPPED")
        self.assertIn("i2", st["jobs"])
        self.assertTrue(os.path.isfile(os.path.join(self.d, "derived", "changes-v2.md")))

    def test_revision_cap_ships_with_caveats(self):
        self.init()
        st = drive(self.d, Fake(reviews=[("REVISE", 4)] * 5))
        self.assertEqual(st["result"]["status"], "SHIPPED_WITH_CAVEATS")
        self.assertEqual(len(st["reviews"]), 1 + room.MAX_REVISIONS)
        self.assertTrue(st["result"]["caveats"])

    def test_the_gates_overrule_a_ship_verdict(self):
        self.init()
        st = drive(self.d, Fake(drop_tag_v1="R1", reviews=[("SHIP", 9), ("SHIP", 9)]))
        first = st["reviews"][0]
        self.assertEqual(first["verdict_ph"], "SHIP")
        self.assertEqual(first["verdict"], "REVISE")
        self.assertTrue(any("R1" in f for f in first["fails"]))
        self.assertEqual(st["result"]["status"], "SHIPPED")

    def test_the_gates_overrule_a_revise_verdict_when_everything_passes(self):
        self.init()
        st = drive(self.d, Fake(reviews=[("REVISE", 8)]))
        self.assertEqual(st["reviews"][0]["verdict"], "SHIP")
        self.assertEqual(st["result"]["status"], "SHIPPED")

    def test_over_budget_final_plan_cannot_ship(self):
        self.init()
        st = drive(self.d, Fake(final_over_budget=True, reviews=[("SHIP", 9)] * 3))
        self.assertIn("S-FINAL-BUDGET-OVER", st["final_checks"])
        self.assertEqual(st["result"]["status"], "SHIPPED_WITH_CAVEATS")

    def test_criterion_floor(self):
        fails = []
        st = {"requirements": [], "deliverable": {"md": os.devnull}, "final_checks": {}}
        data = {"requirements": {}, "blockers": [], "scores": dict((k, 9) for k, _w in room.WEIGHTS)}
        data["scores"]["clarity"] = 4
        fails, _t, total = room.review_gates(st, data)
        self.assertGreater(total, 70)
        self.assertTrue(any("clarity" in f for f in fails))


class Robustness(TempDir):
    def test_invalid_output_is_rerun_once_then_the_seat_is_absent(self):
        self.init()
        st = drive(self.d, Fake(bad_json_always={"k.ux"}))
        self.assertIn("ux", st["absent"])
        self.assertNotIn("ux", st["cast"])
        self.assertEqual(st["jobs"]["k.ux"]["attempts"], 2)
        self.assertEqual(st["result"]["status"], "SHIPPED")

    def test_invalid_output_once_is_rerun_with_the_reasons(self):
        self.init()
        st = drive(self.d, Fake(bad_json_once={"k.developer"}))
        self.assertIn("developer", st["cast"])
        brief = read(st["jobs"]["k.developer"]["prompt"])
        self.assertIn("rejected by the script", brief)
        self.assertTrue(any(f.startswith("k.developer.") and "rejected" in f
                            for f in os.listdir(os.path.join(self.d, "out"))))

    def test_skip_writes_no_output(self):
        self.init()
        fake = Fake()
        run("prompts", "--dir", self.d)
        st = load(self.d)
        fake.do(st, st["jobs"]["in1"])
        run("collect", "--dir", self.d)
        code, out = run("skip", "k.copywriter", "--dir", self.d)
        self.assertEqual(code, 0, out)
        st = drive(self.d, fake)
        self.assertIn("copywriter", st["absent"])

    def test_blocking_question_goes_through_the_gate(self):
        self.init()
        fake = Fake(blocking_question=True)
        run("prompts", "--dir", self.d)
        st = load(self.d)
        fake.do(st, st["jobs"]["in1"])
        run("collect", "--dir", self.d)
        self.assertEqual(load(self.d)["stage"], "gate")
        code, out = run("next", "--dir", self.d)
        self.assertIn("Is November a ramp month?", out)
        ans = os.path.join(self.tmp, "answers.md")
        write(ans, "November is a ramp month.")
        code, out = run("answer", "--file", ans, "--dir", self.d)
        self.assertEqual(code, 0, out)
        st = load(self.d)
        self.assertEqual(st["stage"], "intake")
        self.assertIn("in2", st["jobs"])
        self.assertIn("## Client answers", room.read_brief(st))
        st = drive(self.d, fake)
        self.assertEqual(st["result"]["status"], "SHIPPED")

    def test_answer_assume_uses_the_defaults(self):
        self.init()
        fake = Fake(blocking_question=True)
        run("prompts", "--dir", self.d)
        st = load(self.d)
        fake.do(st, st["jobs"]["in1"])
        run("collect", "--dir", self.d)
        code, out = run("answer", "--assume", "--dir", self.d)
        self.assertEqual(code, 0, out)
        st = load(self.d)
        self.assertEqual(st["stage"], "kickoff")
        self.assertTrue(any("ramp month" in a["text"] for a in st["assumptions"].values()))

    def test_bad_intake_quote_is_rejected_then_accepted_with_a_flag(self):
        self.init()
        run("prompts", "--dir", self.d)
        st = load(self.d)
        job = st["jobs"]["in1"]
        o = outs(job)
        data = {"task_type": "campaign", "requirements": [{"text": "x", "quote": "words that are not there",
                                                           "must": True}], "facts": {}, "cast": []}
        for attempt in range(3):
            write(o["json"], json.dumps(data))
            write(o["md"], "x")
            code, out = run("collect", "--dir", self.d)
            st = load(self.d)
            if st["stage"] != "intake":
                break
        self.assertEqual(attempt, 2)
        self.assertFalse(st["requirements"][0]["quote_ok"])

    def test_init_guards(self):
        code, out = run("init", "--dir", self.d)
        self.assertNotEqual(code, 0)
        self.init()
        code, out = run("init", "--brief", B2B, "--dir", self.d)
        self.assertNotEqual(code, 0)
        self.assertIn("already has a room", out)
        code, out = run("init", "--brief", B2B, "--dir", self.d + "2", "--seats", "google-ads,nobody")
        self.assertNotEqual(code, 0)

    def test_collect_refuses_while_outputs_are_missing(self):
        self.init()
        code, out = run("collect", "--dir", self.d)
        self.assertNotEqual(code, 0)
        self.assertIn("still have no output", out)

    def test_next_resumes_from_disk_at_every_stage(self):
        self.init()
        fake = Fake(over_budget=True, concede=False)
        stages = set()
        for _ in range(100):
            st = load(self.d)
            stages.add(st["stage"])
            if st["stage"] == "done":
                break
            code, out = run("next", "--dir", self.d)
            self.assertEqual(code, 0, out)
            self.assertIn("NEXT", out)
            if room.pending_jobs(st):
                run("prompts", "--dir", self.d)
                st = load(self.d)
                for j in room.pending_jobs(st):
                    fake.do(st, j)
            run("collect", "--dir", self.d)
        self.assertTrue({"intake", "kickoff", "challenge", "respond", "moderate", "resolve", "integrate",
                         "review", "done"} <= stages, stages)


# ---------------------------------------------------------------- the dealer

class Dealer(unittest.TestCase):
    def state(self, cast, seed):
        return {"cast": cast, "seed": seed, "lenses": {}, "targets": {}, "seats": {}, "conflicts": {},
                "lens_relaxed": []}

    def test_lens_guarantees_across_sizes_seeds_and_rounds(self):
        seats = room.seat_ids()
        lens_ids = [l["id"] for l in room.lenses_data()["lenses"]]
        mandatory = room.lenses_data()["mandatory"]
        for n in range(2, len(seats) + 1):
            for seed in range(1, 8):
                cast = seats[:n] if seed % 2 else seats[-n:]
                st = self.state(cast, seed)
                # two seats and two mandatory lenses: a third round must repeat one, so stop at two
                for r in ((1, 2) if n == 2 else (1, 2, 3)):
                    dealt = room.deal_lenses(st, r)
                    self.assertEqual(set(dealt), set(cast))
                    for s, l in dealt.items():
                        self.assertNotEqual(l, room.seat_meta(s)["native_lens"], (n, seed, r, s))
                    for m in mandatory:
                        self.assertIn(m, dealt.values())
                    counts = [list(dealt.values()).count(l) for l in lens_ids]
                    if n >= len(lens_ids):
                        self.assertLessEqual(max(counts) - min(counts), 1)
                    else:
                        self.assertLessEqual(max(counts), 1)
                for s in cast:
                    worn = [st["lenses"][k][s] for k in st["lenses"]]
                    self.assertEqual(len(worn), len(set(worn)), (n, seed, s))
                self.assertEqual(st["lens_relaxed"], [], (n, seed))
                others = [l for l in lens_ids if l not in mandatory]
                used = [sum(1 for k in st["lenses"] for v in st["lenses"][k].values() if v == l) for l in others]
                if n <= len(lens_ids):
                    self.assertLessEqual(max(used) - min(used), 1, (n, seed))

    def test_lens_deal_is_deterministic(self):
        cast = room.seat_ids()[:8]
        a = room.deal_lenses(self.state(cast, 3), 1)
        b = room.deal_lenses(self.state(cast, 3), 1)
        self.assertEqual(a, b)

    def test_targets_cover_everyone_within_bounds(self):
        seats = room.seat_ids()
        for n in range(2, len(seats) + 1):
            for seed in range(1, 8):
                cast = seats[:n] if seed % 2 else seats[-n:]
                st = self.state(cast, seed)
                tg = room.assign_targets(st, 1)
                indeg = {s: 0 for s in cast}
                for s, ts in tg.items():
                    self.assertEqual(len(ts), min(2, n - 1))
                    self.assertNotIn(s, ts)
                    self.assertEqual(len(ts), len(set(ts)))
                    for t in ts:
                        indeg[t] += 1
                self.assertTrue(all(1 <= v <= 3 for v in indeg.values()), (n, seed, indeg))

    def test_targets_prefer_tension_partners(self):
        cast = ["meta-ads", "creative-ops", "seo", "ux", "client-lead", "measurement"]
        tg = room.assign_targets(self.state(cast, 1), 1)
        tension = set(room.seat_meta("meta-ads")["tension"])
        self.assertTrue(set(tg["meta-ads"]) & tension)


# ---------------------------------------------------------------- the deterministic checks

def mini(cast, sidecars, **facts):
    base = {"budget_total": 60000, "currency": "USD", "budget_period": "month", "flight_start": "2026-11-02",
            "flight_end": "2027-01-29", "today": "2026-10-01", "geo": ["US"], "kpis": [],
            "tracking": {"conversion_events": True, "capi_or_enhanced": True, "consent_mode": True}}
    base.update(facts)
    seats = {}
    for s, sc in sidecars.items():
        norm, _e, _w = room.norm_sidecar(sc, cast, True)
        seats[s] = {"sidecar": norm}
    return {"cast": cast, "facts": base, "seats": seats, "today": "2026-10-01"}


def ask(amount, currency="USD", period="month"):
    return {"amount": amount, "currency": currency, "period": period, "source": "ASSUMPTION"}


class Checks(unittest.TestCase):
    def test_budget_over_under_currency_and_period(self):
        st = mini(["google-ads", "meta-ads", "client-lead"],
                  {"google-ads": {"budget_ask": ask(40000)}, "meta-ads": {"budget_ask": ask(30000)}})
        c = room.run_checks(st)
        self.assertEqual(c["S-BUDGET-OVER"]["severity"], "BLOCKER")
        self.assertIn("client-lead", c["S-BUDGET-OVER"]["parties"])
        st = mini(["google-ads"], {"google-ads": {"budget_ask": ask(20000)}})
        self.assertIn("S-BUDGET-UNDER", room.run_checks(st))
        st = mini(["google-ads"], {"google-ads": {"budget_ask": ask(20000, "EUR")}})
        self.assertIn("S-CURRENCY-google-ads", room.run_checks(st))
        st = mini(["google-ads"], {"google-ads": {"budget_ask": ask(180000, period="flight")}})
        c = room.run_checks(st)
        self.assertNotIn("S-BUDGET-OVER", c)
        self.assertNotIn("S-BUDGET-UNDER", c)

    def test_percent_mode(self):
        st = mini(["google-ads", "meta-ads"],
                  {"google-ads": {"budget_ask": {"share_pct": 70, "source": "ASSUMPTION"}},
                   "meta-ads": {"budget_ask": {"share_pct": 50, "source": "ASSUMPTION"}}}, budget_total=None)
        self.assertIn("S-SHARE", room.run_checks(st))

    def test_learning_phase_and_minimum_daily(self):
        meta = {"budget_ask": ask(6000), "forecast": [{"platform": "meta", "budget": 6000, "period": "month",
                                                      "cpa": 60, "units": 5, "optimization_event": "lead",
                                                      "source": "ASSUMPTION"}]}
        c = room.run_checks(mini(["meta-ads"], {"meta-ads": meta}))
        self.assertIn("S-LEARN-meta-ads-meta", c)
        self.assertIn("supports 0 ad set", c["S-LEARN-meta-ads-meta"]["detail"])
        li = {"budget_ask": ask(900), "forecast": [{"platform": "linkedin", "budget": 900, "period": "month",
                                                    "cpc": 9, "units": 4, "source": "ASSUMPTION"}]}
        self.assertIn("S-MINDAILY-linkedin-ads-linkedin", room.run_checks(mini(["linkedin-ads"],
                                                                                {"linkedin-ads": li})))

    def test_funnel_volume_and_cost_are_client_decisions(self):
        g = {"budget_ask": ask(20000), "forecast": [{"platform": "google", "budget": 20000, "period": "month",
                                                     "cpa": 200, "units": 1, "optimization_event": "lead",
                                                     "source": "ASSUMPTION"}]}
        st = mini(["google-ads", "client-lead"], {"google-ads": g},
                  kpis=[{"metric": "MQLs", "target": 400, "unit": "per month", "direction": "min"},
                        {"metric": "CPL", "target": 150, "unit": "USD", "direction": "max"}])
        c = room.run_checks(st)
        self.assertTrue(c["S-FUNNEL-VOLUME"]["client_decision"])
        self.assertTrue(c["S-FUNNEL-COST"]["client_decision"])

    def test_tracking_checks(self):
        g = {"forecast": [{"platform": "google", "budget": 20000, "cpa": 50, "optimization_event": "lead",
                           "source": "ASSUMPTION"}]}
        tr = {"conversion_events": False, "capi_or_enhanced": None, "consent_mode": False}
        c = room.run_checks(mini(["google-ads", "measurement"], {"google-ads": g}, tracking=tr, geo=["UK"]))
        self.assertEqual(c["S-TRACK-EVENTS"]["severity"], "BLOCKER")
        self.assertEqual(c["S-TRACK-CONSENT"]["severity"], "BLOCKER")
        self.assertEqual(c["S-TRACK-SIGNAL"]["severity"], "MAJOR")
        plan = {"tracking_plan": {"conversion_events": "planned", "capi_or_enhanced": "planned",
                                  "consent_mode": "planned", "ready_by": "2026-10-28"}}
        c = room.run_checks(mini(["google-ads", "measurement"], {"google-ads": g, "measurement": plan},
                                 tracking=tr, geo=["UK"]))
        self.assertFalse([k for k in c if k.startswith("S-TRACK")])
        late = {"tracking_plan": dict(plan["tracking_plan"], ready_by="2026-11-20")}
        c = room.run_checks(mini(["google-ads", "measurement"], {"google-ads": g, "measurement": late},
                                 tracking=tr, geo=["US"]))
        self.assertIn("after launch", c["S-TRACK-EVENTS"]["detail"])
        self.assertNotIn("S-TRACK-CONSENT", c)

    def test_timeline_raci_orphans_and_creative_volume(self):
        dev = {"lead_times": [{"item": "server-side tagging", "days": 40, "blocking": True}],
               "owns": [{"key": "landing-page-build", "role": "A"}]}
        ux = {"owns": [{"key": "landing-page-build", "role": "A"}],
              "needs": [{"from": "crm-email", "what": "a nurture flow", "by": "2026-12-01"}]}
        meta = {"budget_ask": ask(30000), "forecast": [{"platform": "meta", "budget": 30000, "cpa": 30,
                                                        "units": 6, "optimization_event": "lead",
                                                        "source": "ASSUMPTION"}]}
        ops = {"capacity": {"assets_per_week": 2}}
        cast = ["developer", "ux", "meta-ads", "creative-ops", "client-lead"]
        c = room.run_checks(mini(cast, {"developer": dev, "ux": ux, "meta-ads": meta, "creative-ops": ops}))
        self.assertEqual(c["S-TIME-developer-server-side-tagging"]["severity"], "BLOCKER")
        self.assertIn("S-RACI-landing-page-build", c)
        self.assertIn("S-ORPHAN-ux-crm-email", c)
        self.assertIn("S-CREATIVE-VOLUME", c)
        self.assertIn("S-NEEDBY-ux-crm-email", c)

    def test_messy_inputs_do_not_fake_or_hide_checks(self):
        # a quarterly target is a quarterly target
        g = {"budget_ask": ask(20000), "forecast": [{"platform": "Google Search", "budget": 20000, "cpa": 50,
                                                     "units": 1, "optimization_event": "lead", "source": "A"}]}
        st = mini(["google-ads", "client-lead"], {"google-ads": g},
                  kpis=[{"metric": "MQLs", "target": 1200, "unit": "per quarter", "direction": "min"},
                        {"metric": "Revenue from online sales", "target": 500000, "unit": "per month",
                         "direction": "min"}])
        self.assertNotIn("S-FUNNEL-VOLUME", room.run_checks(st))
        # a platform written as a product name still gets the learning check
        meta = {"budget_ask": ask(6000), "forecast": [{"platform": "Meta Ads", "budget": 6000, "cpa": 60,
                                                      "units": 5, "optimization_event": "lead", "source": "A"}]}
        self.assertIn("S-LEARN-meta-ads-meta", room.run_checks(mini(["meta-ads"], {"meta-ads": meta})))
        # a currency symbol is not a currency mismatch
        st = mini(["google-ads"], {"google-ads": {"budget_ask": ask(59000, "US$")}})
        self.assertFalse([k for k in room.run_checks(st) if k.startswith("S-CURRENCY")])
        # tracking that is 'in place' or 'live' exists
        gg = {"forecast": [{"platform": "google", "budget": 20000, "cpa": 50, "optimization_event": "lead",
                            "source": "A"}]}
        plan = {"tracking_plan": {"conversion_events": "in place", "capi_or_enhanced": "live",
                                  "consent_mode": "implemented", "ready_by": None}}
        tr = {"conversion_events": None, "capi_or_enhanced": None, "consent_mode": None}
        c = room.run_checks(mini(["google-ads", "measurement"], {"google-ads": gg, "measurement": plan},
                                 tracking=tr, geo=["UK"]))
        self.assertFalse([k for k in c if k.startswith("S-TRACK")], c)
        # an in-flight campaign has no pre-launch lead times
        dev = {"lead_times": [{"item": "a fix", "days": 30, "blocking": True}]}
        st = mini(["developer", "client-lead"], {"developer": dev}, flight_start="2026-09-01")
        self.assertFalse([k for k in room.run_checks(st) if k.startswith("S-TIME")])
        # a share of a known budget counts toward the asks
        st = mini(["google-ads", "meta-ads"], {"google-ads": {"budget_ask": ask(30000)},
                                               "meta-ads": {"budget_ask": {"share_pct": 50, "source": "A"}}})
        self.assertNotIn("S-BUDGET-UNDER", room.run_checks(st))

    def test_final_total_rows_are_not_double_counted(self):
        st = mini(["client-lead"], {})
        lines = [{"line": "Search", "amount": 40000, "currency": "USD", "period": "month", "phase": "2026-11"},
                 {"line": "Social", "amount": 20000, "currency": "USD", "period": "month", "phase": "2026-11"},
                 {"line": "Total media", "amount": 60000, "currency": "USD", "period": "month", "phase": ""}]
        self.assertNotIn("S-FINAL-BUDGET-OVER", room.run_checks(st, final_plan={"budget": lines}))
        lines[0]["currency"] = "$"
        lines[1]["amount"] = 30000
        self.assertIn("S-FINAL-BUDGET-OVER", room.run_checks(st, final_plan={"budget": lines}))

    def test_final_plan_checks(self):
        st = mini(["client-lead"], {})
        c = room.run_checks(st, final_plan={"budget": [{"amount": 50000, "currency": "USD", "period": "month"},
                                                       {"amount": 20000, "currency": "USD", "period": "month"}],
                                            "raci": [{"key": "x", "accountable": ["a", "b"]}]})
        self.assertEqual(c["S-FINAL-BUDGET-OVER"]["severity"], "BLOCKER")
        self.assertIn("S-FINAL-RACI-x", c)

    def test_final_budget_lines_by_month_are_compared_month_by_month(self):
        st = mini(["client-lead"], {})
        lines = [{"amount": a, "currency": "USD", "period": "month", "phase": m}
                 for m in ("2026-11", "2026-12", "2027-01") for a in (40000, 20000)]
        self.assertNotIn("S-FINAL-BUDGET-OVER", room.run_checks(st, final_plan={"budget": lines}))
        lines.append({"amount": 5000, "currency": "USD", "period": "month", "phase": "2026-12"})
        c = room.run_checks(st, final_plan={"budget": lines})
        self.assertIn("in 2026-12", c["S-FINAL-BUDGET-OVER"]["detail"])
        lines = lines[:-1] + [{"amount": 3000, "currency": "USD", "period": "month"}]
        self.assertIn("S-FINAL-BUDGET-OVER", room.run_checks(st, final_plan={"budget": lines}))


# ---------------------------------------------------------------- validation of what the models write

class Validation(TempDir):
    def challenge_job(self, payload, lenient=False, cast=None):
        cast = cast or ["google-ads", "seo", "ux", "client-lead"]
        st = {"cast": cast, "requirements": [{"id": "R1"}, {"id": "R2"}], "limits": {"max_ch": 3},
              "lenses": {"1": {s: "cynical" for s in cast}}, "targets": {"1": {"google-ads": ["seo", "ux"]}}}
        p = os.path.join(self.tmp, "c.json")
        write(p, json.dumps(payload))
        job = {"id": "c1.google-ads", "kind": "challenge", "seat": "google-ads", "round": 1, "outputs": [p]}
        return room.validate_challenge(st, job, lenient)

    def test_caps_downgrades_and_drops(self):
        mk = lambda to, sev="MAJOR", lt="x", rids=None, ev="": {"to": to, "severity": sev, "point": "p",
                                                                  "lens_test": lt, "requirement_ids": rids or [],
                                                                  "evidence": ev}
        data, errors, warnings = self.challenge_job({"challenges": [
            mk("seo", "BLOCKER", rids=["R1"]), mk("ux", "BLOCKER", rids=["R2"]), mk("seo", "BLOCKER"),
            mk("ux", lt=""), mk("nobody"), mk("google-ads"), mk("client-lead"), mk("seo")]})
        chs = data["challenges"]
        self.assertEqual(len(chs), 3)
        self.assertEqual([c["severity"] for c in chs], ["BLOCKER", "MAJOR", "MAJOR"])
        self.assertIn("only one BLOCKER", chs[1]["downgraded"])
        self.assertIn("no requirement id", chs[2]["downgraded"])
        self.assertFalse(errors)
        self.assertTrue(any("lens test" in w for w in warnings))
        data, errors, _w = self.challenge_job({"challenges": [mk("seo", "BLOCKER", ev="see S-BUDGET-OVER")]})
        self.assertEqual(data["challenges"][0]["severity"], "BLOCKER")

    def test_uncovered_targets_are_an_error_then_a_warning(self):
        payload = {"challenges": [{"to": "seo", "point": "p", "lens_test": "x"}]}
        _d, errors, _w = self.challenge_job(payload)
        self.assertTrue(any("ux" in e for e in errors))
        _d, errors, warnings = self.challenge_job(payload, lenient=True)
        self.assertFalse(errors)
        self.assertTrue(any("ux" in w for w in warnings))
        _d, errors, _w = self.challenge_job({"challenges": [{"to": "seo", "point": "p", "lens_test": "x"}],
                                             "clean": [{"to": "UX Lead", "why": "fine"}]})
        self.assertFalse(errors)

    def test_string_ids_and_clean_entries_are_understood(self):
        mk = {"to": "seo", "severity": "BLOCKER", "point": "p", "lens_test": "x", "requirement_ids": "R1, R2"}
        data, errors, _w = self.challenge_job({"challenges": [mk], "clean": ["ux"]})
        self.assertFalse(errors)
        self.assertEqual(data["challenges"][0]["severity"], "BLOCKER")
        self.assertEqual(data["challenges"][0]["requirement_ids"], ["R1", "R2"])

    def test_a_partial_revised_summary_keeps_the_rest(self):
        cast = ["google-ads", "client-lead"]
        full = {"budget_ask": ask(20000), "forecast": [{"platform": "google", "budget": 20000, "cpa": 50,
                                                        "units": 1, "source": "A"}],
                "lead_times": [{"item": "build", "days": 5}]}
        prev, _e, _w = room.norm_sidecar(full, cast, True)
        st = {"cast": cast, "seats": {"google-ads": {"sidecar": prev}}, "inboxes": {"1": {"google-ads": ["CH1.1"]}}}
        md, js = os.path.join(self.tmp, "p.md"), os.path.join(self.tmp, "p.json")
        write(md, LOREM * 2)
        write(js, json.dumps({"responses": [{"id": "ch1.1 (seo)", "verdict": "Conceded", "changes": ["cut"]}],
                              "sidecar": {"budget_ask": ask(15000)}}))
        job = {"id": "p1.google-ads", "kind": "respond", "seat": "google-ads", "round": 1, "outputs": [md, js]}
        data, errors, warnings = room.validate_seat_output(st, job, False)
        self.assertFalse(errors)
        self.assertEqual(data["sidecar"]["budget_ask"]["amount"], 15000)
        self.assertEqual(len(data["sidecar"]["forecast"]), 1)
        self.assertEqual(len(data["sidecar"]["lead_times"]), 1)
        self.assertTrue(any("kept the previous values" in w for w in warnings))

    def test_sidecar_needs_sources_on_numbers(self):
        sc, errors, _w = room.norm_sidecar({"budget_ask": {"amount": "12,500", "currency": "usd"}}, [], False)
        self.assertEqual(sc["budget_ask"]["amount"], 12500)
        self.assertEqual(sc["budget_ask"]["currency"], "USD")
        self.assertTrue(errors)
        sc, errors, warnings = room.norm_sidecar({"budget_ask": {"amount": 1}}, [], True)
        self.assertFalse(errors)
        self.assertTrue(warnings)


class Parsing(unittest.TestCase):
    def test_extract_json(self):
        self.assertEqual(room.extract_json('{"a": 1}'), {"a": 1})
        self.assertEqual(room.extract_json('Here:\n```json\n{"a": 2}\n```\nDone'), {"a": 2})
        self.assertEqual(room.extract_json('noise {"a": 3} noise'), {"a": 3})
        self.assertIsNone(room.extract_json("no json"))

    def test_numbers(self):
        self.assertEqual(room.as_num("60,000"), 60000)
        self.assertEqual(room.as_num("$18k"), 18000)
        self.assertEqual(room.as_num("1210,40"), 1210.40)
        self.assertEqual(room.as_num("4.5%"), 4.5)
        self.assertIsNone(room.as_num("unknown"))
        self.assertIsNone(room.as_num(True))
        # unit words must not leak multipliers, and only the first number counts
        for raw, want in (("60000 per month", 60000), ("$60,000/month", 60000), ("3 campaigns", 3),
                          ("10 working days", 10), ("10 business days", 10), ("400 MQLs", 400),
                          ("USD 18k/month", 18000), ("8/10", 8), ("0/10", 0), ("1.234,56", 1234.56),
                          ("1,234,567", 1234567), ("10m", 1e7), ("5 min", 5)):
            self.assertEqual(room.as_num(raw), want, raw)

    def test_currency_ids_and_platforms(self):
        self.assertEqual(room.norm_currency("US$"), "USD")
        self.assertEqual(room.norm_currency("eur"), "EUR")
        self.assertIsNone(room.norm_currency("$"))
        self.assertEqual(room.match_id("CH1.3 (meta-ads)", {"ch1.3": "CH1.3"}), "CH1.3")
        self.assertEqual(room.match_id("X1 - budget", {"x1": "X1"}), "X1")
        self.assertEqual(room.match_id("R1: KPI", {"r1": "R1"}), "R1")
        self.assertIsNone(room.match_id("nothing", {"x1": "X1"}))
        self.assertEqual(room.id_list("CH1.1, CH1.2; S-BUDGET-OVER"), ["CH1.1", "CH1.2", "S-BUDGET-OVER"])
        self.assertEqual(room.norm_platform("Meta Ads"), "meta")
        self.assertEqual(room.norm_platform("Google Search"), "google")
        self.assertEqual(room.norm_platform("YouTube in Google Ads"), "youtube")
        self.assertEqual(room.norm_verdict("Conceded."), "CONCEDE")
        self.assertEqual(room.norm_verdict("compromised"), "COMPROMISE")
        self.assertEqual(room.norm_verdict("NOTED."), "NOTED")

    def test_consent_geography(self):
        for geo, want in ((["US only (no Canada)"], False), (["US, where it converts"], False), (["UK"], True),
                          (["Germany"], True), (["DE", "FR"], True), (["United Kingdom"], True), (["US"], False)):
            self.assertEqual(room.geo_needs_consent({"geo": geo}), want, geo)

    def test_seat_aliases(self):
        self.assertEqual(room.norm_seat("Meta"), "meta-ads")
        self.assertEqual(room.norm_seat("UX Lead"), "ux")
        self.assertEqual(room.norm_seat("creative ops"), "creative-ops")
        self.assertIsNone(room.norm_seat("the intern"))

    def test_csv_summaries_of_the_examples(self):
        for p in CSVS:
            s = room.summarise_csv(p)
            self.assertIn("**total**", s)
            self.assertNotIn("Could not find", s)
        g = room.summarise_csv(CSVS[0])
        self.assertIn("spend = 'Cost'", g)
        m = room.summarise_csv(CSVS[1])
        self.assertIn("Amount spent", m)

    def test_audit_example_copies_data_and_writes_a_summary(self):
        tmp = tempfile.mkdtemp(prefix="room-test-")
        try:
            d = os.path.join(tmp, "run")
            code, out = run("init", "--brief", AUDIT, "--dir", d, "--data", *CSVS)
            self.assertEqual(code, 0, out)
            self.assertTrue(os.path.isfile(os.path.join(d, "inputs", "summary.md")))
            st = load(d)
            self.assertEqual(len(st["inputs"]), 2)
            code, out = run("prompts", "--dir", d)
            text = read(st["jobs"]["in1"]["prompt"])
            self.assertIn("summary.md", text)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_brief_checks(self):
        tmpl = read(os.path.join(SKILL, "assets", "brief-template.md"))
        warn = room.brief_field_warnings(tmpl)
        self.assertEqual(len(warn), len(room.CRITICAL_BRIEF_FIELDS))
        self.assertEqual(room.brief_field_warnings(read(B2B)), [])
        self.assertEqual(len(room.brief_field_warnings("just a paragraph")), 1)

    def test_tags_and_headings(self):
        self.assertEqual(room.tags_in("met [R1] and [R2, R3] and [D1][R4]"), {"R1", "R2", "R3", "R4", "D1"})
        self.assertEqual(room.tags_in("[R2 and R5] [R6-R8] [r9] [see note] [D2]"),
                         {"R2", "R5", "R6", "R7", "R8", "R9", "D2"})
        self.assertEqual(room.norm_heading("## 4. Budget and channel split [R2]"), "budget and channel split")


class Files(unittest.TestCase):
    def test_templates_complete(self):
        t = room.load_templates()
        self.assertEqual(set(t), set(room.TEMPLATES))

    def test_roster_is_consistent(self):
        r = room.roster()
        ids = [s["id"] for s in r["seats"]]
        self.assertEqual(len(ids), len(set(ids)))
        lens_ids = {l["id"] for l in room.lenses_data()["lenses"]}
        for s in r["seats"]:
            self.assertTrue(os.path.isfile(os.path.join(SKILL, "references", "seats", s["id"] + ".md")), s["id"])
            if s["group"] != "process":
                self.assertIn(s["native_lens"], lens_ids)
            for t in s["tension"]:
                self.assertIn(t, ids)
        for key, owner in r["ownership"].items():
            self.assertIn(owner, ids)
        self.assertEqual(len([s for s in r["seats"] if s["group"] != "process"]), 17)

    def test_seat_files_follow_the_structure(self):
        for s in room.seat_ids():
            text = room.seat_card(s)
            for h in ("## How you think", "## Your blind spots", "## Your checklist", "## Red flags",
                      "## Tensions", "## What you need from others", "## Your contribution by work type"):
                self.assertIn(h, text, (s, h))

    def test_tension_map_pairs_are_real_seats_and_cover_the_roster(self):
        pairs = room.tension_sections()
        ids = set(room.seat_ids())
        self.assertGreaterEqual(len(pairs), 30)
        for a, b in pairs:
            self.assertIn(a, ids)
            self.assertIn(b, ids)
        for s in room.roster()["seats"]:
            for t in s["tension"]:
                self.assertIn(tuple(sorted((s["id"], t))), pairs)

    def test_work_types_have_the_mandatory_headings(self):
        for t in room.TASK_TYPES:
            heads = room.outline_headings(t)
            for h in room.MANDATORY_HEADINGS:
                self.assertIn(h, heads, (t, h))
            self.assertEqual(heads[0], "Executive summary")
            sec = room.work_type_sections(t)
            for k in ("What each seat's kickoff should focus on", "Deliverable outline", "Acceptance criteria"):
                self.assertIn(k, sec, (t, k))

    def test_skill_frontmatter_follows_the_agent_skills_spec(self):
        text = read(os.path.join(SKILL, "SKILL.md"))
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(m)
        keys, fields, cur = [], {}, None
        for line in m.group(1).splitlines():
            km = re.match(r"^([a-z][a-z-]*):\s*(.*)$", line)
            if km:
                cur = km.group(1)
                keys.append(cur)
                fields[cur] = km.group(2)
            elif cur:
                fields[cur] += " " + line.strip()
        self.assertTrue(set(keys) <= {"name", "description", "license", "compatibility", "metadata",
                                      "allowed-tools"}, keys)
        self.assertEqual(fields["name"].strip(), "marketing-room")
        self.assertRegex(fields["name"].strip(), r"^[a-z0-9]+(-[a-z0-9]+)*$")
        desc = fields["description"].replace(">-", "").strip()
        self.assertTrue(0 < len(desc) <= 1024, len(desc))
        self.assertLessEqual(len(fields.get("compatibility", "").strip()), 500)
        self.assertLess(len(text.splitlines()), 500)
        self.assertEqual(os.path.basename(SKILL), "marketing-room")


if __name__ == "__main__":
    unittest.main()
