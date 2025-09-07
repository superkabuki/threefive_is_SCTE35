"""
Example of Editing a Cue.Command and re-encoding
"""

import threefive

# Base64 encoded SCTE-35 Cue
BE64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="

# Create a threefive instance with BE64
cue = threefive.Cue(BE64)

# print the  results as JSON
cue.show()
print(f"\n\nStarting Break Duration was {cue.command.break_duration}\n\n")
# use dot notation to access values and change them
cue.command.break_duration = 120.0

# Run cue.encode to generate new base64 string
# threefive will automatically re-calculate the crc and length vars for you.
cue.encode()

# print the new results as JSON
cue.show()
print(f"\n\nNew Break Duration is {cue.command.break_duration}\n\n")
