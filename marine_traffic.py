import json
import logging
import pyodbc

# Configure logging
logging.basicConfig(filename='scriptDB.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def insert_data_to_db(connection, data):
    """Insert AIS data into the Vessel_Updates table."""
    cursor = connection.cursor()

    for ais_data in data:
        try:
            cursor.execute("""
                INSERT INTO [dbo].[Vessel_Updates]
                ([ProviderID], [ProviderShipID], [IMO], [MMSI], [Name], [CalculatedETA], [ReportedETA], [Latitude], [Longitude], [LastPosDT], [InsertedDT])
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                None,  # Placeholder for ProviderID, you can set a value if you have one
                ais_data.get('ProviderShipID', 10),
                ais_data['IMO'],
                ais_data['MMSI'],
                ais_data['Name'],
                ais_data.get('Predicted Time Of Arrival', None),  # CalculatedETA placeholder
                ais_data.get('Estimated Time Of Arrival', None),
                ais_data.get('Latitude', None),
                ais_data.get('Longitude', None),
                ais_data['InsertedDT'],
                ais_data.get('LastPosDT', None)
            ))
        except pyodbc.Error as e:
            logging.error(f"Error inserting AIS data: {e}")
            continue

    connection.commit()
    cursor.close()
    logging.info("AIS data inserted into the database.")


def main():
    try:
        # Load AIS data from JSON file
        with open('ais_data.json', 'r') as json_file:
            ais_data_list = json.load(json_file)

        # Connect to the SQL Server database
        conn_str = (
            r'DRIVER={SQL Server};'
            r'SERVER=xxxxxxxxxxxx;'  # Replace with your SQL Server IP Address
            r'DATABASE=xxxxxxxxxxx;'
            r'UID=xxxxxxxxx;'
            r'PWD=xxxxxxxxxxxx.;'
        )
        connection = pyodbc.connect(conn_str)
        logging.info("Connected to the SQL Server database.")

        # Insert AIS data to database
        insert_data_to_db(connection, ais_data_list)

        # Close database connection
        connection.close()
        logging.info("Disconnected from the SQL Server database.")

    except FileNotFoundError:
        logging.error("AIS data file not found.")
    except pyodbc.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
