import sys
import os
import django


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blj.settings")
    django.setup()
    from audit.backend import user_interactive

    obj = user_interactive.UserShell(sys.argv)
    try:
        obj.start()
    except KeyboardInterrupt:
        print("bye.")
