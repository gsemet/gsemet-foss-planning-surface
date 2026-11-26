"""The judged rule of each protecting-looking row of the Chief of Staff and Foreman inventories
(round 7, read row by row)."""


def card(*n, name="chief-of-staff"):
    return f"card {name}.md:{', '.join(map(str, n))}"


def floor(*n):
    return f"floor {', '.join(map(str, n))}"


def rule(*parts):
    return "the rule it applies: " + "; ".join(parts)


def refusal(text):
    return f"refusal {text}"


PROCEDURE = "no rule: procedure"
WORDING = "no rule: wording of a message or report"
FACT = "no rule: a fact about the CLI, the host or the forge"
NOBLOCK = "no rule: says what does not block"
GAP = "gap: no card, floor or refusal holds it"

COS: dict[str, str] = {}


def c(ids, text):
    for i in ids.split():
        key = f"C-{i}"
        assert key not in COS, key
        COS[key] = text


c("625 1523 1561 1563", rule(card(3)))
c("590", rule(card(5, 6)))
c("562 584", rule(card(6)))
c("099 944", rule(card(6, 7)))
c("561 564 567 568", rule(card(6, 10)))
c("107 610", rule(card(7)))
c("611 615", rule(card(10, 7)))
c("572 573 575 582 585 587 588 592 595 598 603 605 606 618 945", rule(card(10)))
c("100 540 571 581 593 600 617", rule(card(10), floor(9)))
c("770", rule(floor(9), card(10)))
c("601", rule(card(10, 13)))
c("563", rule(card(10, 17)))
c("025 027 031 078 083 086 095 103 104 126 132 138 273 1168 1505", rule(card(13)))
c("077", rule(card(13), card(21, name="foreman")))
c("312", rule(floor(3), card(13)))
c("365 531 639 679 992 1556 1583", rule(card(14), floor(10)))
c("990", rule(card(14)))
c("1549 1557", rule(card(14, 28)))
c("033", rule(card(28)))
c("1362 1376 1378 1380 1383", rule(card(15)))
c("1334 1355", rule(card(15), floor(6)))
c("882 886 995", rule(card(16)))
c("016 017 834 867 896 967", rule(card(16), floor(10)))
c("878", rule(card(16), floor(9)))
c("884", rule(card(16), refusal("close (rails_idle.py:173 \"cannot close <batch>, something still runs: …\")")))
c("167 180 1464", rule(card(20)))
c("1035 1448 1449", rule(card(21)))
c("003 168 609 930 1117 1232", rule(card(22)))
c("862 1288 1397", rule(card(24)))
c("845", rule(card(24), floor(7)))
c("1148 1192 1399 1400 1402", rule(card(25)))
c("899 952 1014 1021", rule(card(26)))
c("1166", rule(card(27)))
c("316", rule(card(29)))
c("424 971", rule(card(30)))
c("1367 1368 1372", rule(card(31)))
c("091", rule(card(31), floor(6)))
c("053 289 290 291 293 421 960 1421", rule(card(33)))
c("015 393 409 410 425 980 1494", rule(card(35)))
c("835 966", rule(card(37)))
c("307 678 684 685 687 697 698 705 713 732 744 756 772 785 1564", rule(floor(1)))
c("1336 1357", rule(floor(1, 6)))
c("045 052 1222", rule(floor(3)))
c("149", rule(floor(3, 4)))
c("624 1301", rule(floor(3, 9)))
c("047", rule(floor(4)))
c("1386", rule(floor(5)))
c("1330", rule(floor(6)))
c(
    "028 184 189 305 309 434 446 454 515 556 733 788 796 803 807 811 820 823 953 957 1016 1122 "
    "1138 1149 1171 1314 1321 1486",
    rule(floor(7)),
)
c("012 954 1110", rule(floor(7), card(3, name="spec-writer")))
c("1201", rule(card(3, name="spec-writer")))
c("1208", rule(card(15, name="spec-critic")))
c("1142", rule(card(20, name="griller-skill")))
c("1463 1526", rule(card(23, name="griller-skill")))
c(
    "906",
    rule(refusal("take (rails.py:255 \"a new Driver resumes it only with `--note`\")"),
         card(25, name="foreman"), card(35)),
)
c("116 121 357 359 483 769 1385", rule(floor(9)))
c(
    "294 295 1146 1356",
    rule(refusal("order add (commands/orders_release.py:83 \"order add: <rel> has started …\")")),
)
c(
    "300 302 870 879",
    rule(refusal("close (rails_idle.py:173 \"cannot close <batch>, something still runs: …\")")),
)
c(
    "311 532 533",
    rule(refusal("round (rails.py:313 \"<cr>: round limit <n> reached; hand back blocked…\")")),
)
c(
    "404",
    rule(refusal("order waive (commands/orders_waive.py:76 \"--follow-up <backlog folder> names the CR…\")")),
)
c("128", rule(refusal("config (playbook/layers.py:148 \"… are both present: keep one\")")))
c(
    "130",
    rule(refusal("config (playbook/config.py:333 \"\\\"default\\\" resets the value: write it plain…\")")),
)
c("465", rule(refusal("open --direct (commands/opening.py:285)")))
c("903", rule(refusal("take (rails.py:255)")))
c("977 1005", rule(refusal("stale Foreman (core/batch.py:264, exit 3)")))
c("919 920", rule(refusal("order --epoch (commands/orders.py:85)")))
c(
    "947",
    rule(refusal("order qa (commands/orders.py:143 \"a running direct batch takes no QA…\")")),
)
c(
    "512 514 516",
    rule(refusal("order drop (commands/orders.py:275 \"order drop <cr> --note "
                 "trash\\|ready\\|P1..P4…\")")),
)
c("511", rule(refusal("order drop (commands/orders_drop.py:40, already dropped)")))
c("1324", rule(refusal("order after (commands/orders_after.py:85, the release CR)")))
c(
    "1364",
    rule(refusal("open (rails_release.py:157 \"a release grant needs a batch budget…\")")),
)
c("1029", rule(refusal("file (lifecycle/backlog.py:70 \"the request has no short title…\")")))
c(
    "024 158 253 277 347 362 369 411 489 492 537 543 621 668 748 895 907 921 925 946 965 998 "
    "1022 1046 1049 1170 1209 1213 1233 1241 1437 1444 1455 1493 1554 1591",
    PROCEDURE,
)
c("822", "no rule: procedure (routing)")
c("368", "no rule: procedure (who syncs; a holder is not stopped: floor 10)")
c(
    "098 111 242 249 263 279 482 496 688 692 766 805 881 1011 1012 1054 1056 1065 1070 1373 "
    "1428 1552 1575",
    WORDING,
)
c(
    "034 133 141 221 235 236 239 271 287 298 381 384 458 738 875 876 897 1174 1298 1377 1384 "
    "1431 1440 1489 1517 1518 1524 1529 1550",
    FACT,
)
c("112 148 360 366 371 372 871 1553", NOBLOCK)
c("006 304 885", GAP)

FM: dict[str, str] = {}


def f(ids, text):
    for i in ids.split():
        key = f"FM-{i}"
        assert key not in FM, key
        FM[key] = text


def fm(*n):
    return card(*n, name="foreman")


f("022", rule(fm(31)))
f("026", GAP)
f("028", rule(refusal("pause (commands/closing.py:85 \"<batch> is already paused\")")))
f("060", rule(card(18, name="stack-driver")))
f("065", rule(fm(13), floor(3)))
f("078", rule(refusal("check_slot (rails.py:57)"), floor(9)))
f("086", rule(fm(14), floor(7)))
f("089", rule(refusal("order after (commands/orders_after.py:91)")))
f("105 314", rule(fm(22)))
f("112 187 197", rule(fm(13)))
f("125", rule(fm(31)))
f("155", rule(fm(16)))
f("157", rule(card(3)))
f("B052", rule(fm(29), floor(7)))
f("173 178", rule(refusal("check_shape (rails_release.py:192)"), fm(15)))
f("212", rule(fm(13), card(18, name="stack-driver")))
f("254", rule(fm(14)))
f("284", rule(floor(5), fm(22)))
f("293", rule(fm(22, 23)))
f("318", rule(floor(1), fm(20)))
f("332", rule(refusal("take (rails.py:261 \"<cr> still has an agent recorded\")")))
f("337 399 410 412 416 455 458 459", rule(fm(25)))
f("342", rule(floor(7), fm(14), refusal("refuse_held (stacks.py:23)")))
f("347", rule(fm(14), refusal("check_slot (rails.py:57)")))
f(
    "356",
    rule(refusal("refuse_held (stacks.py:23 \"<cr> is held (order <O>): only the user's `order unhold <cr>` releases it\")")),
)
f("367", rule(fm(15)))
f("378", rule(fm(14), floor(5, 7)))
f("384", rule(floor(3, 9)))
f("424", rule(refusal("check_budget (rails.py:222)"), floor(9)))
f("427 430 575", rule(fm(29)))
f("460", rule(fm(21)))
f("501 503", rule(floor(6), fm(14)))
f("509", rule(floor(6, 7)))
f("514 515", rule(floor(7), refusal("check_granted_fix (rails_release.py:108)")))
f("516 517 518", rule(fm(22), card(6, 7, 8, 9, 10)))
f("522 543", rule(fm(22), floor(2)))
f("524", rule(floor(2), card(6)))
f("559 560 561 563 565 579 580 591 592", rule(fm(22), floor(9)))
f("598 604", "no rule: the retro critic's procedure")
