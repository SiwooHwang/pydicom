import os
from pydicom.uid import ExplicitVRLittleEndian

from pynetdicom import AE, debug_logger, evt
from pynetdicom.sop_class import CTImageStorage

debug_logger()

def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    print(ds.file_meta)

    # Save the dataset using the SOP Instance UID as the filename
    base_dir = os.getcwd()
    fpath = os.path.join(base_dir, ds.StudyInstanceUID)

    if os.path.isdir(fpath):
        ds.save_as(fpath + "/" + ds.SOPInstanceUID, write_like_original=False)
        return 0x0000

    os.makedirs(fpath, exist_ok=True)
    ds.save_as(fpath + "/" + ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000


handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()
ae.ae_title=b'siwoo(public)'
ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
ae.add_supported_context('1.2.840.10008.1.1')
ae.start_server(('192.200.0.22', 1040), block=True, evt_handlers=handlers)
