from pydicom.dataset import Dataset
from pynetdicom.pdu_primitives import UserIdentityNegotiation

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

debug_logger()

# Initialise the Application Entity
ae = AE()
ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
ae.add_requested_context("1.2.840.10008.1.2")
# ae.ae_title = b'RECON'

ds = Dataset()
ds.QueryRetrieveLevel = 'SERIES'
# # Unique key for PATIENT level
# ds.PatientID = '4151'
ds.PatientID = ''
ds.PatientName = ''
ds.StudyInstanceUID = ''
ds.StudyDescription = ''
ds.SeriesInstanceUID = ''
ds.SeriesDescription = ''
# ds.instanceNumber = ''

userIdentity = UserIdentityNegotiation()
# userIdentity.user_identity_type = 2
# userIdentity.primary_field = b'test'
# userIdentity.secondary_field = b'1'
negotationItem = []
negotationItem.append(userIdentity)
# Associate with peer AE at IP 127.0.0.1 and port 11112
# assoc = ae.associate('192.168.100.2', 104, ae_title=b'Test')
assoc = ae.associate('192.168.0.4', 1040, ae_title=b'hutom7')
if assoc.is_established:
    # Send the C-FIND request
    responses = assoc.send_c_find(
        ds, PatientRootQueryRetrieveInformationModelFind)
    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04X}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')
