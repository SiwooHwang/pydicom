from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, evt, StoragePresentationContexts, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove

debug_logger()

ae = AE()

ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
ae.supported_contexts = StoragePresentationContexts


def handle_store(event):
    """Handle a C-STORE service request"""
    ds = event.dataset
    ds.file_meta = event.file_meta

    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Ignore the request and return Success
    return 0x000


handlers = [(evt.EVT_C_STORE, handle_store)]

ae.ae_title = b'STORE_SCP'
scp = ae.start_server(('0.0.0.0', 4242),
                      block=False, evt_handlers=handlers)

ds = Dataset()
# ds.QueryRetrieveLevel = 'SERIES'
ds.QueryRetrieveLevel = 'IMAGE'
ds.PatientID = 'ANONYMIZE_0212'
ds.SeriesInstanceUID = '1.3.6.1.4.1.43276.1.3.2019120419.031354.966.1569.0744'
ds.SOPInstanceUID = '1.3.6.1.4.1.43276.1.4.2019120419.031354.966.1569.0745'

assoc = ae.associate('192.168.1.190', 4242)

if assoc.is_established:
    responses = assoc.send_c_move(
        ds, 'STORE_SCP', PatientRootQueryRetrieveInformationModelMove)
    for (status, identifier) in responses:
        if status:
            print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')
    assoc.release()
else:
    print('Association rejected, aborted or never connected')
