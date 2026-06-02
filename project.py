"""
It's actually a solid idea for this project specifically
— your runtime flow is already well-defined in DEV_NOTES, so a skeleton project.py
would just be translating that into function stubs with comments.
It costs almost nothing and gives you a concrete scaffold to hang everything else on.

The risk with skeleton-first is when the design is still fuzzy — you end up rewriting it.
But you've already done that thinking. Your startup sequence (load → reconcile → persist → main menu loop)
is linear and stable enough that sketching it won't mislead you.

The one thing to avoid: don't let the skeleton tempt you into fleshing out cli.py or handlers.py prematurely.

Keep the stubs as pass or raise NotImplementedError and go build the domain models.
The skeleton's job is orientation, not implementation order.

So: domain models are still where the real work starts, but a skeleton project.py alongside that is fine.
"""


def main(): ...


if __name__ == "__main__":
    main()
