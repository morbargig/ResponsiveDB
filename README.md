# MongoDB Controller Script

This Python script includes a class `Mongod` which provides methods to interact with MongoDB, including starting and stopping the MongoDB service, finding data, adding data, updating passwords and usernames, and updating users to unfollow. It handles the MongoDB connection and disconnection as needed.

## Usage

### Initialization:

Before using the script, ensure you have MongoDB installed and running on your system.

### Running the Script:

1. **Start MongoDB Service:**
   - Run the script to start the MongoDB service using the `start()` method.

2. **Interacting with MongoDB:**
   - Use the provided methods of the `Mongod` class to perform various operations:
     - `findData(_id, collaction=None, collactionName=None)`: Find data by ID.
     - `add_data(data, collactionName)`: Add new data to the collection.
     - `passwordOf(_id, pk=False)`: Get the password of a user by ID.
     - `pkOf(_id)`: Get the primary key of a user by ID.
     - `updatePassword(user_name, new_password)`: Update the password of a user.
     - `updateUserName(user_name, new_user_name)`: Update the username of a user.
     - `updateUsersToUnfollow(user_name, users, add=True)`: Update users to unfollow for a specific user.

3. **Stop MongoDB Service:**
   - After using the script, stop the MongoDB service using the `stop()` method.

### Example Usage:

```python
m = Mongod()
m.add_data({"_id" : "mor_bargig", "user_name": "mor_bargig" , "pk" : 873268 },"clients")
print(m.updateUsersToUnfollow("mor_bargig", [("Aran", 12345678, False)]))
```

Notes
This script provides a convenient way to manage MongoDB operations using Python.
Ensure you have the necessary permissions and MongoDB configurations set up before running the script.
