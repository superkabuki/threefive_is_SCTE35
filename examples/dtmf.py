"""
SCTE35 DTMF Descriptor Example

Usage:
    python3 dtmf.py

"""


from threefive3 import Cue

if __name__ == "__main__":
    DTMF = "/DAsAAAAAAAAAP/wDwUAAABef0/+zPACTQAAAAAADAEKQ1VFSbGfMTIxIxGolm0="
    cue=Cue(DTMF)
    # Display results
    print('\nDecoded:\n')
    cue.show()
    # Encode to hex
    print(f'\nEncoded as Hex:\n\n{cue.hex()}')
