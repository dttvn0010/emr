from peewee import *
from playhouse.postgres_ext import JSONField

from constants import(
    EncounterClass,
    EncounterStatus,
    ObservationValueType,
    DiagnosisRole,
    ConditionSeverity
)

db = PostgresqlDatabase(
    'emr', user='admin', password='abc@123',
    host='103.124.94.100', port=5432
)

class BaseModel(Model):
    class Meta:
        database = db

class Department(BaseModel):
    parent = ForeignKeyField('self', backref='children', null=True)
    name = CharField(max_length=200)

class Role(BaseModel):
    name = CharField(max_length=100)
    description = CharField(max_length=200)
    privileges = CharField(max_length=2000)

class User(BaseModel):
    username = CharField(max_length=100, unique=True)
    full_name = CharField(max_length=100)
    email = CharField(max_length=100)
    phone = CharField(max_length=20)
    address = CharField(max_length=200)
    password = CharField(max_length=100)
    role = ForeignKeyField(Role, null=True)

class Staff(BaseModel):
    department = ForeignKeyField(Department, null=True)
    employee_number = CharField(max_length=30, unique=True)
    full_name = CharField(max_length=100)
    user = ForeignKeyField(User)

class Building(BaseModel):
    department = ForeignKeyField(Department)
    name = CharField(max_length=200)

class Room(BaseModel):
    building = ForeignKeyField(Building)
    number = CharField(max_length=50)

class Bed(BaseModel):
    room = ForeignKeyField(Room)
    number = CharField(max_length=50)

class CodeSystem(BaseModel):
    parent = ForeignKeyField('self', null=True)
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)
    attributes = JSONField(null=True)

class Patient(BaseModel):
    user = ForeignKeyField(User, null=True)
    insurance_number = CharField(max_length=30, unique=True)
    insurance_number_startdate = DateTimeField()
    insurance_number_enddate = DateTimeField()
    national_identifier = CharField(max_length=30)
    full_name = CharField(max_length=100)
    gender = CharField(max_length=10)
    temp_address = CharField(max_length=200)
    permanent_address = CharField(max_length=200)
    phone = CharField(max_length=20)
    email = CharField(max_length=100)
    date_of_birth = DateTimeField()

class Encounter(BaseModel):
    department = ForeignKeyField(Department)
    patient = ForeignKeyField(Patient)
    mrn = CharField(max_length=20, unique=True)
    class_code = CharField(choices=EncounterClass.choices())
    type_ = ForeignKeyField(CodeSystem, null=True)
    main_practitioner = ForeignKeyField(Staff, null=True)
    room = ForeignKeyField(Room, null=True)
    bed = ForeignKeyField(Bed, null=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    status = CharField(choices=EncounterStatus.choices())

class Diagnosis(BaseModel):
    encounter = ForeignKeyField(Patient)
    role = CharField(choices=DiagnosisRole.choices())
    icd = ForeignKeyField(CodeSystem, null=True)
    serverity = CharField(choices=ConditionSeverity.choices(), null=True)
    text = CharField(max_length=200)

class ServiceCategory(BaseModel):
    parent = ForeignKeyField('self', null=True)
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)

class Service(BaseModel):
    category = ForeignKeyField(ServiceCategory)
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)
    price_norm = IntegerField()
    insurance_pctg = FloatField()
    attributes = JSONField(null=True)

class Procedure(BaseModel):
    service = ForeignKeyField(Service)
    patient = ForeignKeyField(Patient)
    encounter = ForeignKeyField(Patient)
    authored_on = DateTimeField()
    requester = ForeignKeyField(User)
    performed_on = DateTimeField(null=True)
    report_issued_on = DateTimeField(null=True)
    reporter = ForeignKeyField(User, null=True)
    result = CharField(max_length=500)
    conclusion = CharField(max_length=500)
    note = CharField(max_length=500)

    amount_total = IntegerField()
    amount_insurance = IntegerField()
    amount_patient_paid = IntegerField()

class ProcedurePerformer(BaseModel):
    procedure = ForeignKeyField(Procedure)
    role_code = ForeignKeyField(CodeSystem, null=True)
    role_desc = CharField(max_length=200)
    performer = ForeignKeyField(Staff)

class MedicationCategory(BaseModel):
    parent = ForeignKeyField('self', null=True)
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)

class MedicationUnit(BaseModel):
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)

class MedicationRoute(BaseModel):
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)

class MedicationManufacturer(BaseModel):
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)
    country = ForeignKeyField(CodeSystem, null=True)

class Medication(BaseModel):
    category = ForeignKeyField(MedicationCategory)
    code = CharField(max_length=20, unique=True)
    name = CharField(max_length=200)
    price_norm = IntegerField()
    unit = ForeignKeyField(MedicationUnit)
    route = ForeignKeyField(MedicationRoute)
    manufacturer = ForeignKeyField(MedicationManufacturer)
    insurance_pctg = FloatField()
    attributes = JSONField(null=True)

class MedicationStock(BaseModel):
    department = ForeignKeyField(Department, null=True)
    name = CharField(max_length=100)
    location = CharField(max_length=200)

class MedicationStockQuantity(BaseModel):
    stock = ForeignKeyField(MedicationStock)
    medication = ForeignKeyField(Medication)
    avail_quantity = IntegerField()
    last_updated = DateTimeField()

class MedicationRequestGroup(BaseModel):
    patient = ForeignKeyField(Patient)
    encounter = ForeignKeyField(Patient)
    authored_on = DateTimeField()
    requester = ForeignKeyField(User)

class MedicationRequest(BaseModel):
    group = ForeignKeyField(MedicationRequestGroup)
    medication = ForeignKeyField(Medication)
    dose = FloatField()
    instruction = CharField(max_length=500)

class MedicationRequestRate(BaseModel):
    medication_request = ForeignKeyField(MedicationRequest)
    rate = FloatField()
    time_of_day = CharField(max_length=50)
    note = CharField(max_length=200)

class MedicationDispenseGroup(BaseModel):
    request_group = ForeignKeyField(MedicationRequestGroup, null=True)
    packager = ForeignKeyField(Staff, null=True)
    checker = ForeignKeyField(Staff, null=True)
    dispensed_on = DateTimeField()
    amount_total = IntegerField()
    amount_insurance = IntegerField()
    amount_paid_by_patient = IntegerField()

class MedicationDispense(BaseModel):
    group = ForeignKeyField(MedicationDispenseGroup)
    medication = ForeignKeyField(Medication)
    quantity = FloatField()
    stock = ForeignKeyField(MedicationStock, null=True)
    amount_total = IntegerField()
    amount_insurance = IntegerField()
    amount_patient_paid = IntegerField()

class Observation(BaseModel):
    patient = ForeignKeyField(Patient)
    encounter = ForeignKeyField(Patient)
    code = ForeignKeyField(CodeSystem)
    issued_on = DateTimeField()
    recorder = ForeignKeyField(User, null=True)
    note = CharField(max_length=500)
    value_type = CharField(choices=ObservationValueType.choices())
    value_quantity = FloatField()
    value_unit = CharField(max_length=50)
    value_code = ForeignKeyField(CodeSystem, null=True)
    value_text = CharField(max_length=500)
    value_datetime = DateTimeField()