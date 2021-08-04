import os

from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, StoragePresentationContexts, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove

# Implement the evt.EVT_C_MOVE handler


def handle_move(event):
    """Handle a C-MOVE request event."""
    ds = event.identifier

    if 'QueryRetrieveLevel' not in ds:
        # Failure
        yield 0xC000, None
        return

    # get_known_aet() is here to represent a user-implemented method of
    #   getting known AEs, for this example it returns a dict with the
    #   AE titles as keys
    known_aet_dict = get_known_aet()
    try:
        (addr, port) = known_aet_dict[event.move_destination]
    except KeyError:
        # Unknown destination AE
        yield (None, None)
        return

    # Yield the IP address and listen port of the destination AE
    yield (addr, port)

    # Import stored SOP Instances
    instances = []
    matching = []
    fdir = './_data'
    for fpath in os.listdir(fdir):
        instances.append(dcmread(os.path.join(fdir, fpath)))

    if ds.QueryRetrieveLevel == 'PATIENT':
        if 'PatientID' in ds:
            matching = [
                inst for inst in instances if inst.PatientID == ds.PatientID
            ]

        # Skip the other possible attributes...

    # Skip the other QR levels...

    # Yield the total number of C-STORE sub-operations required
    yield len(matching)

    # Yield the matching instances
    for instance in matching:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        # Pending
        yield (0xFF00, instance)


handlers = [(evt.EVT_C_MOVE, handle_move)]

# Create application entity
ae = AE()
# ae.ae_title = b'STORE_SCP'
print("open server")

# Add the requested presentation contexts (Storage SCU)
ae.requested_contexts = StoragePresentationContexts
# Add a supported presentation context (QR Move SCP)
ae.add_supported_context(PatientRootQueryRetrieveInformationModelMove)

# Start listening for incoming association requests
# ae.start_server(('127.0.0.1', 4242), evt_handlers=handlers)
ae.ae_title=b'hutom7'
ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
ae.add_supported_context('1.2.840.10008.1.1')
ae.start_server(('192.168.100.7', 1040), block=True, evt_handlers=handlers)
