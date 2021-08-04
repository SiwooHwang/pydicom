from pydicom.dataset import Dataset

from pynetdicom import AE, evt, StoragePresentationContexts, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove

debug_logger()


# def handle_store(event):
#     """Handle a C-STORE request event."""
#     ds = event.dataset
#     ds.file_meta = event.file_meta

#     # Save the dataset using the SOP Instance UID as the filename
#     # ds.save_as(ds.SOPInstanceUID, write_like_original=False)

#     # Return a 'Success' status
#     return 0x0000


# handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

ae.supported_contexts = StoragePresentationContexts

# Start our Storage SCP in non-blocking mode, listening on port 11120
ae.ae_title = b'STORE_SCP'
# scp = ae.start_server(('127.0.0.1', 4242),
#                       block=False, evt_handlers=handlers)

# Create out identifier (query) dataset
ds = Dataset()
ds.QueryRetrieveLevel = 'PATIENT'
# Unique key for PATIENT level
ds.PatientID = 'ANONYMIZE_0209'
# Unique key for STUDY level
# ds.StudyInstanceUID = '1.3.6.1.4.1.43276.1.2.2019120419.035201.138.1569.28736'
# Unique key for SERIES level
ds.SeriesInstanceUID = '1.3.6.1.4.1.43276.1.3.2019120419.033832.674.1569.18863'
ds.SOPInstanceUID = '1.3.6.1.4.1.43276.1.4.2019120419.033832.674.1569.18864'

# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('192.168.1.190', 4242)

if assoc.is_established:
    # Use the C-MOVE service to send the identifier
    responses = assoc.send_c_move(
        ds, b'STORE_SCP', PatientRootQueryRetrieveInformationModelMove)
    for (status, identifier) in responses:
        if status:
            print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')
