from pydicom.uid import ExplicitVRLittleEndian

from pynetdicom import AE, debug_logger, evt
from pynetdicom.sop_class import CTImageStorage

debug_logger()


def handle_store(event):
    """Handle EVT_C_STORE events."""
    return 0x0000


handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()
ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
ae.start_server(('192.168.1.240', 108), block=True, evt_handlers=handlers)
