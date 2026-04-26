class PIMService:
    def __init__(self, api_client):
        self.client = api_client
        self.endpoints = {
            "employees": "/web/index.php/api/v2/pim/employees"
        }

    def add_new_employee(self, first_name, last_name, employee_id):
        """Creates employee via API for fast test setup."""
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "employeeId": employee_id
        }
        return self.client.post(self.endpoints["employees"], data=payload)

    def delete_employee(self, employee_ids: list):
        """
        Removes employees by ID to keep the environment clean.
        OrangeHRM usually expects a list of internal IDs in the payload.
        """
        # Note: In a real environment, you might need the internal 'empNumber'
        # but many wrappers allow deletion via this endpoint.
        payload = {"ids": employee_ids}
        return self.client.request.delete(self.endpoints["employees"], data=payload)