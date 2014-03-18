from announcements.models import Password
import sys

Password(sys.argv[1])
print("New password added to the announcements: %s" % sys.argv[1])
