import webview
import os
import sqlite3
import base64
import uuid

class Api:

	def delete_appliance_canvas(self, canvas_id):
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
				
			# Insert the appliance and image path into the database
			query = "DELETE FROM canvas WHERE id = ?;"
			cursor.execute(query, (canvas_id,))
			connection.commit()  # Commit the transaction
				
			return {'message': 'Removed successfully.'}
			
		except sqlite3.Error as e:
			return {'error': 'Error occured please try again'}
			
		finally:
			if cursor:
				cursor.close()
			if connection:
				connection.close()


	def update_appliance_canvas(self, simulation_id ,room_id, appliance_id, from_room, canvas_id):
		try:
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()

			restricted_appliance_id_1 = ['91', '92', '93', '94']
			restricted_appliance_id_2 = ['77', '78', '79', '80']

			restricted_rooms_id_1 = [
	            'bath1', 'bath2', 'bed2Right', 'bathright1', 'bathright2',
	            'bed1right', 'bed1', 'bathLeft1', 'bathLeft2', 'bedroomLeft22',
	            'bedroomRight11', 'bathRight1', 'bathRight2', 'bedroomRight22',
	            'bedroomLeft1', 'bedroomLeft2', 'bathLeft', 'bedroomRight1',
	            'bedroomRight2', 'bathRight', 'bathRight123', 'bedroom1T2',
	            'bedroom3T2', 'bedroom4T2', 'bedroom6T2', 'bedroom7T2',
	            'bedroom9T2', 'masterbed1T2', 'masterbed2T2', 'masterbed3T2',
	            'bedroomLeft11', 'bed1dup1', 'bed2dup1', 'master1dup1', 'master2dup1', 'bed1B2', 'bed2B2','bed3B2',
	            'masterbedB3', 'bedB3', 'bed2B3', 'bathB2', 'tb1tg', 'tb2tg', 'tb3tg',
	            'bath1dup1', 'bath2dup1','bath3dup1','bath4dup1', 'masterbathB3','bathB3'
	       		]

			restricted_rooms_id_2 = [
	            'bath1', 'bath2', 'bathright1', 'bathright2',
	            'bed1right', 'bathLeft1', 'bathLeft2','bathRight1', 'bathRight2', 'bathLeft',
	            'bedroomRight2','bathB2', 'tb1tg', 'tb2tg', 'tb3tg',
	            'bath1dup1', 'bath2dup1','bath3dup1','bath4dup1', 'masterbathB3','bathB3'
	       		]	       		


			if room_id in restricted_rooms_id_1 and appliance_id in restricted_appliance_id_1:
				return {'error': 'Unable to transfer appliance to this room, for safety purposes.'}

			if room_id in restricted_rooms_id_2 and appliance_id in restricted_appliance_id_2:
				return {'error': 'Unable to transfer appliance to this room, for safety purposes.'}			

			# Insert the appliance and image path into the database
			query = "UPDATE canvas SET room_id = ? WHERE id = ?;"
			cursor.execute(query, (room_id, canvas_id))
			connection.commit()  # Commit the transaction
					
			return {'message': 'Transfered successfully.'}
			
		except sqlite3.Error as e:
			return {'error': 'Error occured please try again'}
			
		finally:
			if cursor:
				cursor.close()
			if connection:
				connection.close()


	def add_appliance_canvas(self, simulation_id, room_id, appliance_id):
	    try:
	    	# Connect to the SQLite database
	        connection = sqlite3.connect('ecoenergy.db')
	        cursor = connection.cursor()

	        restricted_appliance_id_1 = ['91', '92', '93', '94']
	        restricted_appliance_id_2 = ['77', '78', '79', '80']

	        restricted_rooms_id_1 = [
	            'bath1', 'bath2', 'bed2Right', 'bathright1', 'bathright2',
	            'bed1right', 'bed1', 'bathLeft1', 'bathLeft2', 'bedroomLeft22',
	            'bedroomRight11', 'bathRight1', 'bathRight2', 'bedroomRight22',
	            'bedroomLeft1', 'bedroomLeft2', 'bathLeft', 'bedroomRight1',
	            'bedroomRight2', 'bathRight', 'bathRight123', 'bedroom1T2',
	            'bedroom3T2', 'bedroom4T2', 'bedroom6T2', 'bedroom7T2',
	            'bedroom9T2', 'masterbed1T2', 'masterbed2T2', 'masterbed3T2',
	            'bedroomLeft11', 'bed1dup1', 'bed2dup1', 'master1dup1', 'master2dup1', 'bed1B2', 'bed2B2','bed3B2',
	            'masterbedB3', 'bedB3', 'bed2B3', 'bathB2', 'tb1tg', 'tb2tg', 'tb3tg',
	            'bath1dup1', 'bath2dup1','bath3dup1','bath4dup1', 'masterbathB3','bathB3'
	       		]
	       	restricted_rooms_id_2 = [
	            'bath1', 'bath2', 'bathright1', 'bathright2',
	            'bed1right', 'bathLeft1', 'bathLeft2','bathRight1', 'bathRight2', 'bathLeft',
	            'bedroomRight2','bathB2', 'tb1tg', 'tb2tg', 'tb3tg',
	            'bath1dup1', 'bath2dup1','bath3dup1','bath4dup1', 'masterbathB3','bathB3'
	       		]
	       	if room_id in restricted_rooms_id_1 and appliance_id in restricted_appliance_id_1:
	       		return {'error': 'Unable to transfer appliance to this room, for safety purposes.'}
	       	if room_id in restricted_rooms_id_2 and appliance_id in restricted_appliance_id_2:
	       		return {'error': 'Unable to transfer appliance to this room, for safety purposes.'}

	        # Insert the appliance and image path into the database
	        query = "INSERT INTO canvas(simulation_id, room_id, appliance_id) VALUES(?, ?, ?);"
	        cursor.execute(query, (simulation_id, room_id, appliance_id))
	        connection.commit()  # Commit the transaction

	        return {'message': 'Appliance added to room.'}
	    except sqlite3.Error as e:
	    	return {'error': 'Error occurred, please try again'}
	    finally:
	    	if cursor:
	    		cursor.close()
	    	if connection:
	    		connection.close()
	    # except sqlite3.Error as e:
	    # 	return {'error': 'Error occurred, please try again'}

		# finally:
		# 	if cursor:
		# 		cursor.close()
		# 	if connection:
		# 		connection.close()


	def create_room(self, room_name, simulation_id):
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
				
			# Insert the appliance and image path into the database
			query = "INSERT INTO room(name, simulation_id) VALUES(?, ?);"
			cursor.execute(query, (room_name, simulation_id))
			connection.commit()  # Commit the transaction
				
			return {'message': 'Room created successfully.'}
			
		except sqlite3.Error as e:
			return {'error': 'Error occured please try again'}

		finally:
			if cursor:
				cursor.close()
			if connection:
				connection.close()


	def create_simulation(self, name):
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
				
			# Insert the appliance and image path into the database
			query = "INSERT INTO simulation(name) VALUES(?);"
			cursor.execute(query, (name,))
			connection.commit()  # Commit the transaction
			session_id = cursor.lastrowid
				
			return {'message': 'Simulation created successfully.', 'session_id': session_id}
			
		except sqlite3.Error as e:
			return {'error': 'Error occured please try again'}
			
		finally:
			if cursor:
				cursor.close()
			if connection:
				connection.close()

	def upload_image(self, base64_image, appliance, name, watt):
			try:
				# Decode the base64 image
				image_data = base64.b64decode(base64_image)
				image_name = f"{str(uuid.uuid4())}.png"
				
				# Specify the upload folder path
				upload_folder = os.path.join(os.getcwd(), 'assets/uploads')
				
				# Create the folder if it doesn't exist
				if not os.path.exists(upload_folder):
					os.makedirs(upload_folder)
				
				# Full file path for the image
				file_path = os.path.join(upload_folder, image_name)
				
				# Write the image to the folder
				with open(file_path, 'wb') as f:
					f.write(image_data)
				
				# Connect to the SQLite database
				connection = sqlite3.connect('ecoenergy.db')
				cursor = connection.cursor()
				
				# Insert the appliance and image path into the database
				query = "INSERT INTO sub_appliance(appliance_id, image, name, watt) VALUES(?, ?, ?, ?);"
				cursor.execute(query, (appliance, image_name, name, watt))
				connection.commit()  # Commit the transaction
				
				return f'file://{file_path}'
			
			except sqlite3.Error as e:
				return f"Error: {e}"
			
			finally:
				if cursor:
					cursor.close()
				if connection:
					connection.close()

	def appliance_list(self):
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
			
			# Execute the query to get main appliance data
			appliance_query = "SELECT id, name, image FROM appliance;"
			cursor.execute(appliance_query)
			appliances = cursor.fetchall()
			appliance_columns = [description[0] for description in cursor.description]

			result = ""
			for appliance in appliances:
				result += f"""<div style="style="background:#f9f9f9""><br><br><br>
				"""
				appliance_data = {appliance_columns[i]: appliance[i] for i in range(len(appliance))}
				
				# Execute the query to get sub-appliance data for each appliance
				sub_appliance_query = """
				SELECT id, image, watt, name
				FROM sub_appliance
				WHERE appliance_id = ?;
				"""
				cursor.execute(sub_appliance_query, (appliance_data['id'],))
				sub_appliances = cursor.fetchall()
				sub_appliance_columns = [description[0] for description in cursor.description]

				# Generate the main image and dropdown structure
				result += f"""
				<div class="dropdown dropup">
					    <img data-bs-placement="top" title="{appliance_data['name']}" draggable="false" data-is-update="0" id="s{appliance_data['id']}" data-bs-toggle="dropdown" aria-expanded="false" style="width:25px; height:30px; padding:5px;" src="assets/vectors/{appliance_data['image']}" />
    					<ul class="dropdown-menu" style="background:white; z-index: 9999!important; position: absolute; top: -50px;" aria-labelledby="s{appliance_data['id']}">
						<div class="d-flex p-1 text-center">
				"""
				for sub_appliance in sub_appliances:
					sub_appliance_data = {sub_appliance_columns[i]: sub_appliance[i] for i in range(len(sub_appliance))}
					result += f"""
							<div>
								<img data-bs-toggle="tooltip" data-bs-placement="top" title="{sub_appliance_data['name']} - {sub_appliance_data['watt']} W" draggable="true" id="{sub_appliance_data['id']}" style="max-height:35px;margin:4px" src="assets/uploads/{sub_appliance_data['image']}"/>
							</div>
					"""
				result += """
						</div>
					</ul>
				</div>
				"""
				result += f"""</div>
				"""
			
			return {'message': result}
		
		except sqlite3.Error as e:
			return {'message': f"Error: {e}"}
		finally:
			cursor.close()
			connection.close()

	def navbar(self):

		# Connect to the SQLite database (it will create the file if it doesn't exist)
		connection = sqlite3.connect('ecoenergy.db')
		cursor = connection.cursor()
			
		# Execute the query
		cursor.execute("SELECT * FROM simulation ORDER BY name;")
		rows = cursor.fetchall()  # Fetch all rows from the query result
		columns = [description[0] for description in cursor.description]  # Get column names

		# Return the fetched data as a string (for simplicity)

		r = ""

		simulations = ""

		for row in rows:
			row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
			simulations += f"""
						 <li><p onclick="setID('{row_data['name']}', '{row_data['id']}');" class="text-white" >{row_data['name']}</p></li>
						"""
		r += """
				<div class="nav-item dropdown">
						<a style="color:black!important" class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
							List of House
						</a>
						<ul class="dropdown-menu p-2 text-white" aria-labelledby="navbarDropdownMenuLink" style="background:gray;width:230px!important">
						"""
		r +=   simulations

		r += """
						</ul>
					</div>
		"""


		return {'message': r}
	# def navbar(self):

	# 	# Connect to the SQLite database (it will create the file if it doesn't exist)
	# 	connection = sqlite3.connect('ecoenergy.db')
	# 	cursor = connection.cursor()
			
	# 	# Execute the query
	# 	cursor.execute("SELECT * FROM simulation ORDER BY name;")
	# 	rows = cursor.fetchall()  # Fetch all rows from the query result
	# 	columns = [description[0] for description in cursor.description]  # Get column names

	# 	# Return the fetched data as a string (for simplicity)

	# 	r = ""

	# 	simulations = ""

	# 	for row in rows:
	# 		row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
	# 		simulations += f"""
	# 					 <li><p onclick="setID('{row_data['name']}', '{row_data['id']}');" class="text-white" >{row_data['name']}</p></li>
	# 					"""
	# 	r += """<div class="container-fluid">
			
	# 		<div >
	# 			<button class="navbar-toggler text-white" style="color:white" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
	# 			<span class="navbar-toggler-icon text-white" style="color:white"></span>
	# 			</button>

	# 		</div>
			
	# 		<div class="collapse navbar-collapse" id="navbarNavDropdown">
	# 			<ul class="navbar-nav text-white">
	# 				<li class="nav-item">
	# 					<a class="nav-link active" aria-current="page" href="index.html">Home</a>
	# 				</li>

				

	# 				<li class="nav-item">
	# 					<span class="nav-link" onclick="showComparative();" >Comparative Analysis</span>
	# 				</li>

	# 				<li class="nav-item">
	# 					<span class="nav-link" onclick="showTarget();" >Target Consumption</span>
	# 				</li>

	# 				<li class="nav-item dropdown">
	# 					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
	# 						List of House
	# 					</a>
	# 					<ul class="dropdown-menu p-2 text-white" aria-labelledby="navbarDropdownMenuLink" style="background:#CE3A00;width:230px!important">
	# 					"""
	# 	r +=   simulations

	# 	r += """
	# 					</ul>
	# 				</li>
	# 			</ul>
	# 		</div>


	# 		<div class="row">
	# 		<div class="col-6">
			
	# 		</div>
	# 		<div class="col-6">
				
	# 		</div>
	# 		</div>
			
	# 		 <a class="navbar-brand text-white" href="index.html">Eco Energy Tracker</a>

	# 	</div>"""


	# 	return {'message': r}


	def fetch_appliance(self):
		try:
			# Connect to the SQLite database (it will create the file if it doesn't exist)
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
			
			# Execute the query
			cursor.execute("SELECT * FROM sub_appliance;")
			rows = cursor.fetchall()  # Fetch all rows from the query result
			columns = [description[0] for description in cursor.description]  # Get column names

			# Return the fetched data as a string (for simplicity)
			result = ""
			for row in rows:
				row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
				result += f"""<tr>
								<td>{row_data['id']} - {row_data['appliance_id']}</td>
								<td>{row_data['name']}</td>
								<td>{row_data['watt']}</td>
								<td> <img src="assets/uploads/{row_data['image']}" style="width:60px" />  </td>
							</tr>"""
	  
			return {'message': result}
		
		except sqlite3.Error as e:
			return {'message': f"Error: {e}"}
		finally:
			cursor.close()
			connection.close()

	def fetch_room(self, simulation_id):
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
			
			# Query to fetch room and canvas details
			query = """SELECT room.id AS roomId, room.name AS roomName, sub_appliance.image AS applianceImage, 
			sub_appliance.id AS applianceImageId, sub_appliance.name AS applianceName, canvas.id AS canvasRow, 
			sub_appliance.watt AS watt
			FROM canvas 
			 JOIN room ON room.id = canvas.room_id
			JOIN sub_appliance ON sub_appliance.id = canvas.appliance_id
			WHERE canvas.simulation_id = ?;"""

			cursor.execute(query, (simulation_id,))
			rows = cursor.fetchall()  # Fetch all rows from the query result

			columns = [description[0] for description in cursor.description]  # Get column names

			# Group images by roomId
			grouped_data = {}
			for row in rows:
				row_data = {columns[i]: row[i] for i in range(len(row))}
				room_id = row_data['roomId']
				canvas_id = row_data['canvasRow']  # Fetch the canvas.id
				watt = row_data['watt'] 
				
				if room_id not in grouped_data:
					grouped_data[room_id] = {
						'roomName': row_data['roomName'],
						'canvasRow': canvas_id,
						'images': [],
						'watt': watt

					}
				# Append image, image_id, and canvas_id to the list of images
				grouped_data[room_id]['images'].append((row_data['applianceImage'], row_data['applianceImageId'], canvas_id, watt, row_data['applianceName']))

			if(simulation_id == '85'):
				# Map HTML IDs to room IDs
				room_id_map = {
					'bedroomLeft11': 'bedroomLeft11',
					'bathLeft2': 'bathLeft2',
					'bathLeft1': 'bathLeft1',
					'bedroomLeft22': 'bedroomLeft22',
					'laundryLeft': 'laundryLeft',
					'kitchenDiningLeft': 'kitchenDiningLeft',
					'livingAreaLeft': 'livingAreaLeft',
					'bedroomRight11': 'bedroomRight11',
					'bathRight1': 'bathRight1',
					'bathRight2': 'bathRight2',
					'bedroomRight22': 'bedroomRight22',
					'laundryRight': 'laundryRight',
					'livingAreaRight': 'livingAreaRight',
					'kitchenDiningRight': 'kitchenDiningRight'
				}

				# Generate HTML

				result = """
				<div class="row mt-3">
				    <!-- Left side of duplex -->
				    <div class="col-6">
				      <!-- Bedrooms Row -->
				      <div class="row">
				        <div class="col-4 room yellow-door-color">Bedroom 1 <div id="bedroomLeft11" class="droptarget">{bedroomLeft11}</div>
				        <div class="sleeping-door yellow-door-color" style="right:0px;bottom:0px"></div></div>
				        <div class="col-3">
				        	<!-- Bathrooms Row -->
					      <div class="row">
					        <div class="col-12 room blue-door-color">Bath 1 <div id="bathLeft1" class="droptarget">{bathLeft1}</div>
					        <div class="standing-door blue-door-color" style="top:8px;right:0px"></div></div>
					        <div class="col-12 room blue-door-color">Bath 2 <div id="bathLeft2" class="droptarget">{bathLeft2}</div>
					        <div class="sleeping-door blue-door-color" style="left:15px;bottom:0px"></div></div>
					      </div>
				        </div>
				        <div class="col-5 room yellow-door-color">Bedroom 2 <div id="bedroomLeft22" class="droptarget">{bedroomLeft22}</div>
				        <div class="sleeping-door  yellow-door-color" style="left:0px;bottom:0px"></div></div>
				      </div>
				      <!-- Laundry -->
				      <div class="row">
				      	<div class="col-8"></div>
				        <div class="col-4 room blue-door-color">Laundry 1<div id="laundryLeft" class="droptarget">{laundryLeft}</div>
				         <div class="standing-door blue-door-color" style="left:0px;bottom:10px"></div>
				          <div class="sleeping-door blue-door-color" style="left:10px;bottom:0px"></div></div>
				      </div>
				      <!-- Kitchen / Dining -->
				      <div class="row">
				        <div class="col-8 room  red-door-color">Kitchen / Dining 1 <div id="kitchenDiningLeft" class="droptarget">{kitchenDiningLeft}</div>
				         <div class="sleeping-door  red-door-color" style="left:200px;bottom:0px"></div></div>
				      	<!-- Living Area -->
				        <div class="col-4 room pt-2">Living Area 1<div id="livingAreaLeft" class="droptarget">{livingAreaLeft}</div>
				       </div>
				      </div>
				    </div>

				    <!-- Right side of duplex -->
				    <div class="col-6">
				      <!-- Bedrooms Row -->
				      <div class="row">
				        <div class="col-4 room yellow-door-color">Bedroom 3<div id="bedroomRight11" class="droptarget">{bedroomRight11}</div>
				        <div class="sleeping-door  yellow-door-color" style="right:0px;bottom:0px"></div></div>
				        <div class="col-3">
				        <!-- Bathrooms Row -->
					      <div class="row">
					        <div class="col-12 room blue-door-color">Bath 2 <div id="bathRight1" class="droptarget">{bathRight1}</div>
					         <div class="standing-door blue-door-color" style="top:8px;left:0px"></div></div>
					        <div class="col-12 room blue-door-color">Bath 3<div id="bathRight2" class="droptarget">{bathRight2}</div>
					        <div class="sleeping-door blue-door-color" style="right:15px;bottom:0px"></div></div>
					      </div>
				        </div>
				        <div class="col-5 room yellow-door-color">Bedroom 4<div id="bedroomRight22" class="droptarget">{bedroomRight22}</div>
				         <div class="sleeping-door  yellow-door-color" style="left:0px;bottom:0px"></div></div>
				      </div>
				      <!-- Laundry -->
				      <div class="row">

				      		<div class="col-4 room blue-door-color">Laundry 2<div id="laundryRight" class="droptarget">{laundryRight}</div>
				      		  <div class="standing-door blue-door-color" style="right:0px;bottom:10px"></div>
				          <div class="sleeping-door blue-door-color" style="right:10px;bottom:0px"></div></div>
				      		<div class="col-8"></div>
				        
				      </div>
				      <!-- Kitchen / Dining -->
				      <div class="row">
				      	<!-- Living Area -->
				        <div class="col-4 room pt-2 orange-door-color">Living Area 2<div id="livingAreaRight" class="droptarget">{livingAreaRight}</div>
				          
				        </div>
				        <div class="col-8 room red-door-color">Kitchen / Dining 2<div id="kitchenDiningRight" class="droptarget">{kitchenDiningRight}</div>
				        <div class="sleeping-door  red-door-color" style="right:200px;bottom:0px"></div></div>
				      </div>
				      
				    </div>
				  </div>
				"""
			if(simulation_id == '84'):
				# Map HTML IDs to room IDs
				room_id_map = {
					'bed2': 'bed2',
					'kitchen1': 'kitchen1',
					'bath1': 'bath1',
					'bath2': 'bath2',
					'dining1': 'dining1',
					'bed1': 'bed1',
					'living': 'living',
					'porch1': 'porch1',
					'bed2Right': 'bed2Right',
					'kitchen2': 'kitchen2',
					'bathright1': 'bathright1',
					'bathright2': 'bathright2',
					'dining2': 'dining2',
					'bed1right': 'bed1right',
					'living2': 'living2',
					'porch2': 'porch2'
				}
				result = """
				<div class="row m-3" style="width: 100%;">
					<div class="col-6">
						<!-- First row: Bed 2, Bath, Kitchen -->
						<div class="row">
							<div class="col-6 room container yellow-door-color" >Bedroom 1  <div id="bed2" class="droptarget">{bed2} </div> 
							<div class="sleeping-door  yellow-door-color" style="right:0px;bottom:0px"></div> </div>
							<div class="col-6 room red-door-color">Kitchen 1 <div id="kitchen1" class="droptarget">{kitchen1}</div>
							<div class="sleeping-door  red-door-color" style="right:0px;top:0px"></div>
							</div>
						</div>
						<!-- Second row: Bath, Dining -->
						<div class="row">
							<div class="col-6">
								<div class="row">
									<div class="col-9 room blue-door-color container" style="border: 2px solid black">Bath 1 <div id="bath1" class="droptarget">{bath1}</div>
									<div class="standing-door blue-door-color" style="right:0px;top:0px"></div></div>
									<div class="col-9 room blue-door-color" style="border: 2px solid black">Bath 2<div  id="bath2" class="droptarget">{bath2}</div>
									<div class="sleeping-door blue-door-color" style="right:0px;bottom:0px"></div></div>
								</div>
							</div>
							<div class="col-6 room red-door-color container">Dining 1 <div id="dining1" class="droptarget">{dining1}</div>
							<div class="standing-door red-door-color" style="left:0px;bottom:0px"></div></div>
						</div>
						<!-- Third row: Bed 1, Living -->
						<div class="row">
							<div class="col-5 room  yellow-door-color" >Bed 2<div id="bed1" class="droptarget">{bed1}</div>
							<div class="sleeping-door  yellow-door-color" style="top:0px;right:0px"></div></div>
							<div class="col-7 room orange-door-color" >Living 1<div id="living" class="droptarget">{living}</div>
							<div class="sleeping-door orange-door-color" style="left:0px;bottom:0px"></div>
							</div>
						</div>
						<!-- Fourth row: Porch -->
						<div class="row">
							<div class="col-8"></div>
							<div class="col-4 room orange-door-color" >Porch 1<div id="porch1" class="droptarget">{porch1}</div>
							<div class="sleeping-door orange-door-color" style="left:0px;bottom:0px"></div></div>
						</div>
					</div>
					<div class="col-6">
						<!-- First row: Bed 2, Bath, Kitchen -->
						<div class="row">
							<div class="col-6 room yellow-door-color">Bed 3 <div id="bed2Right" class="droptarget">{bed2Right}</div>
							<div class="sleeping-door  yellow-door-color" style="right:0px;bottom:0px"></div></div>
							<div class="col-6 room  red-door-color">Kitchen 2<div id="kitchen2" class="droptarget">{kitchen2}</div>
							<div class="sleeping-door  red-door-color" style="right:0px;top:0px"></div></div>
						</div>
						<!-- Second row: Bath, Dining -->
						<div class="row">
							<div class="col-6">
								<div class="row">
									<div class="col-9 room blue-door-color" style="border: 2px solid black">Bath 3 <div id="bathright1" class="droptarget">{bathright1}</div>
									<div class="standing-door blue-door-color" style="right:0px;top:0px"></div></div>
									<div class="col-9 room blue-door-color" style="border: 2px solid black">Bath 4<div id="bathright2" class="droptarget">{bathright2}</div>
									<div class="sleeping-door blue-door-color" style="right:0px;bottom:0px"></div></div>
								</div>
							</div>
							<div class="col-6 room red-door-color" >Dining 2<div id="dining2" class="droptarget">{dining2}</div>
							<div class="standing-door red-door-color" style="left:0px;bottom:0px"></div></div>
						</div>
						<!-- Third row: Bed 1, Living -->
						<div class="row">
							<div class="col-5 room yellow-door-color">Bedroom 4<div id="bed1right" class="droptarget">{bed1right}</div>
							<div class="sleeping-door  yellow-door-color" style="top:0px;right:0px"></div></div>
							<div class="col-7 room orange-door-color">Living 2<div id="living2" class="droptarget">{living2}</div>
							<div class="sleeping-door orange-door-color" style="left:0px;bottom:0px"></div></div>
						</div>
						<!-- Fourth row: Porch -->
						<div class="row">
							<div class="col-8"></div>
							<div class="col-4 room orange-door-color">Porch 2<div id="porch2" class="droptarget">{porch2}</div>
							<div class="sleeping-door orange-door-color" style="left:0px;bottom:0px"></div></div>
						</div>
					</div>
				</div>
				"""

			if(simulation_id == '86'):
				# Map HTML IDs to room IDs Duplex 3
				room_id_map = {
					'bedroomLeft1': 'bedroomLeft1',
					'bedroomLeft2': 'bedroomLeft2',
					'bathLeft': 'bathLeft',
					'kitchenLeft': 'kitchenLeft',
					'diningLeft': 'diningLeft',
					'livingRoomLeft': 'livingRoomLeft',
					'porchLeft': 'porchLeft',
					'bedroomRight1': 'bedroomRight1',
					'bedroomRight2': 'bedroomRight2',
					'bathRight': 'bathRight',
					'kitchenRight': 'kitchenRight',
					'diningRight': 'diningRight',
					'livingRoomRight': 'livingRoomRight',
					'porchRight': 'porchRight'
				}
				result = """
				<div class="row mt-3">
			    <!-- Left side of duplex -->
			    <div class="col-6">
			      <!-- Bedrooms -->
			      <div class="row">
			        <div class="col-4 room yellow-door-color">Bedroom 1 <div id="bedroomLeft1" class="droptarget">{bedroomLeft1}</div>
			         <div class="standing-door  yellow-door-color" style="right:0px;bottom:0px"></div></div>
			         <div class="col-4 room blue-door-color">Bath 1<div id="bathLeft" class="droptarget">{bathLeft}</div>
			         <div class="standing-door blue-door-color" style="right:0px;bottom:0px"></div></div>
			        <div class="col-4 room red-door-color">Kitchen 1 <div id="kitchenLeft" class="droptarget">{kitchenLeft}</div>
			        <div class="sleeping-door  red-door-color" style="left:0px;top:0px"></div></div>
			      </div>
			      <!-- Bath and Kitchen -->
			      <div class="row">
			       <div class="col-4 room yellow-door-color">Bedroom 2 <div id="bedroomLeft2" class="droptarget">{bedroomLeft2}</div>
			       <div class="standing-door  yellow-door-color" style="right:0px;top:0px"></div></div>
			       <div class="col-8">
			       	<div class="col-12 room red-door-color">Dining 1 <div id="diningLeft" class="droptarget">{diningLeft}</div>
			       	<div class="standing-door red-door-color" style="left:0px;top:0px"></div></div>
			       <div class="col-12 room orange-door-color">Living Room 1 <div id="livingRoomLeft" class="droptarget">{livingRoomLeft}</div>
 					<div class="sleeping-door orange-door-color" style="bottom:0px;left:20px"></div>
			       </div>
			       </div>
			      </div>
			      <!-- Dining and Living Room -->
			      <div class="row">
			        
			        
			      </div>
			      <!-- Porch -->
			      <div class="row">
			        <div class="col-7 room orange-door-color">Porch 1 <div id="porchLeft" class="droptarget">{porchLeft}</div>
			        </div>
			        <div class="col-5 "></div>
			      </div>
			    </div>

			    <!-- Right side of duplex -->
			    <div class="col-6">
			      <!-- Bedrooms -->
			      <div class="row">
			              <div class="col-4 room red-door-color">Kitchen 2 <div id="kitchenRight" class="droptarget">{kitchenRight}</div>
			        <div class="sleeping-door  red-door-color" style="right:0px;top:0px"></div></div>
			        <div class="col-4 room blue-door-color">Bath 2 <div id="bathRight" class="droptarget">{bathRight}</div>
			       <div class="standing-door blue-door-color" style="left:0px;bottom:0px"></div></div>
			        <div class="col-4 room yellow-door-color">Bedroom 3 <div id="bedroomRight1" class="droptarget">{bedroomRight1}</div>
			        <div class="standing-door yellow-door-color" style="left:0px;bottom:0px"></div></div>

			
			        
			      </div>
			      <!-- Dining and Living Room -->
			      <div class="row">

			      </div>
			      <!-- Bath and Kitchen -->
			      <div class="row">
						
						<div class="col-8">
							<div class="col-12 room red-door-color">Dining 2 <div id="diningRight" class="droptarget">{diningRight}</div>
							<div class="standing-door red-door-color" style="right:0px;top:0px"></div></div>
				        	<div class="col-12 room orange-door-color">Living Room 2<div id="livingRoomRight" class="droptarget">{livingRoomRight}</div>
							<div class="sleeping-door orange-door-color" style="bottom:0px;right:20px"></div>
				        	</div> 
						</div>
						<div class="col-4 room yellow-door-color ">Bedroom 4 <div id="bedroomRight2" class="droptarget">{bedroomRight2}</div>
						<div class="standing-door yellow-door-color" style="left:0px;top:0px"></div></div>
			      </div>

			      <!-- Porch -->
			      <div class="row">
			        <div class="col-5 "></div>
			        <div class="col-7 room orange-door-color">Porch 2 <div id="porchRight" class="droptarget">{porchRight}</div>
			        </div>
			      </div>
			    </div>
			  </div>

				"""

			if(simulation_id == '87'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'outdoorDiningLeft': 'outdoorDiningLeft',
					'outdoorLivingLeft': 'outdoorLivingLeft',
					'diningLeft1': 'diningLeft1',
					'livingRoomLeft87': 'livingRoomLeft87',
					'kitchen': 'kitchen',
					'pantryLeft': 'pantryLeft',
					'mudRoomLeft': 'mudRoomLeft',
					'garageLeft': 'garageLeft',
					'techCenterRight': 'techCenterRight',
					'bathRight123': 'bathRight123',
					'officeGuestRoomRight': 'officeGuestRoomRight',
					'entryPorch': 'entryPorch',
					'foyer': 'foyer'
				}
				result = """
				 <div class="row mt-3">
				    <div class="col-6 room red-door-color">Outdoor Dining Area
				      <div id="outdoorDiningLeft" class="droptarget">{outdoorDiningLeft}</div>
				    </div>
				    <div class="col-6 room orange-door-color">Outdoor Living Area
				      <div id="outdoorLivingLeft" class="droptarget">{outdoorLivingLeft}</div>
				    </div>
				  </div>
				  <div class="row">
				   <div class="col-6">
				     <div class="col-12 room red-door-color">Dining
				      <div id="diningLeft1" class="droptarget">{diningLeft1}</div>
				    </div>
				    <div class="col-12 room red-door-color">Kitchen
				      <div id="kitchen" class="droptarget">{kitchen}</div>
				    </div>
				    </div>
				    <div class="col-6 py-4 room orange-door-color">Living Room
				      <div id="livingRoomLeft87" class="droptarget">{livingRoomLeft87}</div>
				       
				    </div>
				  </div>
				  <div class="row">
				    <div class="col-2 room red-door-color">Pantry
				      <div id="pantryLeft" class="droptarget">{pantryLeft}</div>
				      <div class="sleeping-door red-door-color" style="right:0px;top:0px"></div>
				    </div>
				     <div class="col-2">
				      
				    </div>
				    <div class="col-2 room green-door-color">Mud Room
				      <div id="mudRoomLeft" class="droptarget">{mudRoomLeft}</div>
				      <div class="sleeping-door green-door-color" style="right:0px;bottom:0px"></div>
				    </div>
				    <div class="col-6">
				      
				    </div>
				  </div>
				 
				  <div class="row">
					    <div class="col-6 room py-5 violet-door-color">
					    	<br>
					    	2 Car Garage
					      <div id="garageLeft" class="droptarget">{garageLeft}</div>
					    	<br>

					    </div>
					    <div class="col-6 row">
						    <div class="col-6 room violet-door-color">Tech Center
						      <div id="techCenterRight" class="droptarget">{techCenterRight}</div>
						    </div>
						    <div class="col-6 room blue-door-color">Bath
						      <div id="bathRight123" class="droptarget">{bathRight123}</div>
						      <div class="standing-door blue-door-color" style="left:0px;bottom:0px"></div>
						    </div>
						    <div class="col-6 room green-door-color">Foyer
						      <div id="foyer" class="droptarget">{foyer}</div>
						     
						    </div>
						    <div class="col-6 room  yellow-door-color">Office / Guest Room
						      <div id="officeGuestRoomRight" class="droptarget">{officeGuestRoomRight}</div>
						      <div class="sleeping-door yellow-door-color" style="left:0px;top:0px"></div>
						    </div>
						    <div class="col-6 room  orange-door-color">Entry Porch
						      <div id="entryPorch" class="droptarget">{entryPorch}</div>
						    </div>
				    	</div>

				  </div>

				"""

			if(simulation_id == '88'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'bedroom1T2': 'bedroom1T2',
					'hallway2T2': 'hallway2T2',
					'bedroom3T2': 'bedroom3T2',

					'bedroom4T2': 'bedroom4T2',
					'hallway5T2': 'hallway5T2',
					'bedroom6T2': 'bedroom6T2',

					'bedroom7T2': 'bedroom7T2',
					'hallway8T2': 'hallway8T2',
					'bedroom9T2': 'bedroom9T2'
					,
					'masterbed1T2': 'masterbed1T2',
					'balcony1T2': 'balcony1T2',

					'masterbed2T2': 'masterbed2T2',
					'balcony2T2': 'balcony2T2',

					'masterbed3T2': 'masterbed3T2',
					'balcony3T2': 'balcony3T2'
				}
				result = """
				<div class="row mt-3">


						<div class="col-4">
							<div class="row">
								<div class="col-6">
							      	
							    </div>

							    <div class="col-6 room yellow-door-color">Bedroom 1
						      		<div id="bedroom1T2" class="droptarget">{bedroom1T2}</div>
						      		<div class="sleeping-door  yellow-door-color" style="bottom:0px;left:0px"></div>
						    	</div>


								 <div class="col-6 room green-door-color">Hallway 1
							      	<div id="hallway2T2" class="droptarget">{hallway2T2}</div>
							    </div>

						    	 <div class="col-6 room yellow-door-color">Bedroom 2
						      		<div id="bedroom3T2" class="droptarget">{bedroom3T2}</div>
						      		<div class="standing-door  yellow-door-color" style="top:0px;left:0px"></div>
						    	</div>
							</div>
						</div>

						<div class="col-4">
							<div class="row">
								<div class="col-6">
							      	
							    </div>

							    <div class="col-6 room yellow-door-color">Bedroom 3
						      		<div id="bedroom4T2" class="droptarget">{bedroom4T2}</div>
						      		<div class="sleeping-door  yellow-door-color" style="bottom:0px;left:0px"></div>
						    	</div>


								 <div class="col-6 room green-door-color">Hallway 2
							      	<div id="hallway5T2" class="droptarget">{hallway5T2}</div>
							    </div>

						    	 <div class="col-6 room yellow-door-color">Bedroom 4
						      		<div id="bedroom6T2" class="droptarget">{bedroom6T2}</div>
						      		<div class="standing-door  yellow-door-color" style="top:0px;left:0px"></div>
						    	</div>
							</div>
						</div>
						<div class="col-4">
							<div class="row">
								<div class="col-6">
							      	
							    </div>

							    <div class="col-6 room yellow-door-color">Bedroom 5
						      		<div id="bedroom7T2" class="droptarget">{bedroom7T2}</div>
						      		<div class="sleeping-door  yellow-door-color" style="bottom:0px;left:0px"></div>
						    	</div>


								 <div class="col-6 room green-door-color">Hallway 3
							      	<div id="hallway8T2" class="droptarget">{hallway8T2}</div>
							    </div>

						    	 <div class="col-6 room yellow-door-color">Bedroom 6
						      		<div id="bedroom9T2" class="droptarget">{bedroom9T2}</div>
						      		<div class="standing-door  yellow-door-color" style="top:0px;left:0px"></div>
						    	</div>
							</div>
						</div>
						<div class="col-4">
							<div class="row">
					
							    <div class="col-12 room yellow-door-color">Master's Bedroom 1
						      		<div id="masterbed1T2" class="droptarget">{masterbed1T2}</div>
						      		<div class="sleeping-door  yellow-door-color" style="top:0px;left:0px"></div>
						    	</div>
						    	<div class="col-8">
						      		
						    	</div>
						    	<div class="col-4 room green-door-color">Balcony 1
						      		<div id="balcony1T2" class="droptarget">{balcony1T2}</div>
						    	</div>

							</div>
						</div>
						<div class="col-4">
							<div class="row">
					
							    <div class="col-12 room yellow-door-color">Master's Bedroom 2
						      		<div id="masterbed2T2" class="droptarget">{masterbed2T2}</div>
						      		<div class="sleeping-door  yellow-door-color" style="top:0px;left:0px"></div>
						    	</div>
						    	<div class="col-8">
						      		
						    	</div>
						    	<div class="col-4 room green-door-color">Balcony 2
						      		<div id="balcony2T2" class="droptarget">{balcony2T2}</div>
						    	</div>

							</div>
						</div>
						<div class="col-4">
							<div class="row">
					
							    <div class="col-12 room yellow-door-color">Master's Bedroom 3
						      		<div id="masterbed3T2" class="droptarget">{masterbed3T2}</div>
						      		<div class="sleeping-door  yellow-door-color" style="top:0px;left:0px"></div>
						    	</div>
						    	<div class="col-8">
						      		
						    	</div>
						    	<div class="col-4 room green-door-color">Balcony 3
						      		<div id="balcony3T2" class="droptarget">{balcony3T2}</div>
						    	</div>

							</div>
						</div>





				
				  </div>
				"""			


			if(simulation_id == '89'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {

					'bed1dup1': 'bed1dup1',
					'bed2dup1': 'bed2dup1',
					'master1dup1': 'master1dup1',
					'master2dup1': 'master2dup1',

					'bath1dup1': 'bath1dup1',
					'bath2dup1': 'bath2dup1',
					'bath3dup1': 'bath3dup1',
					'bath4dup1': 'bath4dup1',

					'kitchen1dup1': 'kitchen1dup1',
					'kitchen2dup1': 'kitchen2dup1',

					'laundry1dup1': 'laundry1dup1',
					'laundry2dup1': 'laundry2dup1',

					'dining1dup1': 'dining1dup1',
					'dining2dup1': 'dining2dup1',

					'living1dup1': 'living1dup1',
					'living2dup1': 'living2dup1',

					'porch1dup1': 'porch1dup1',
					'porch2dup1': 'porch2dup1'
				}
				result = """
				<div class="row mt-3">


						<div class="col-12">
							<div class="row">
	

							    <div class="col-3 room yellow-door-color">Bedroom 1
						      		<div id="bed1dup1" class="droptarget">{bed1dup1}</div>
						      		<div class="standing-door yellow-door-color" style="bottom:0px;right:0px"></div>
						    	</div>


								 <div class="col-3 ">
								 <div class="room p-4 yellow-door-color">Master Bedroom 1
							      	<div id="master1dup1" class="droptarget">{master1dup1}</div>
							      	<div class="standing-door yellow-door-color" style="top:0px;left:0px"></div>
							      	<div class="standing-door yellow-door-color" style="bottom:0px;left:0px"></div>
							      </div>
							    </div>

							   <div class="col-3 ">
								 <div class="room yellow-door-color p-4">Master Bedroom 2
							      	<div id="master2dup1" class="droptarget">{master2dup1}</div>
							      	<div class="standing-door yellow-door-color" style="top:0px;right:0px"></div>
							      	<div class="standing-door yellow-door-color" style="bottom:0px;right:0px"></div>
							      </div>
							    </div>

							    <div class="col-3 room yellow-door-color">Bedroom 2
						      		<div id="bed2dup1" class="droptarget">{bed2dup1}</div>
						      		<div class="standing-door yellow-door-color" style="bottom:0px;left:0px"></div>
						    	</div>


							</div>
						</div>

						<div class="col-12">
							<div class="row">
	  							<div class="col-2">
						    	</div>

							    <div class="col-2 room blue-door-color">Bathroom 1
						      		<div id="bath1dup1" class="droptarget">{bath1dup1}</div>
						      		<div class="standing-door blue-door-color" style="top:0px;left:0px"></div>
						    	</div>


								 <div class="col-2 room blue-door-color">Bathroom 2
							      	<div id="bath2dup1" class="droptarget">{bath2dup1}</div>
							      	<div class="sleeping-door blue-door-color" style="top:0px;right:0px"></div>
							    </div>

							    <div class="col-2 room blue-door-color">Bathroom 3
							      	<div id="bath3dup1" class="droptarget">{bath3dup1}</div>
							      	<div class="sleeping-door blue-door-color" style="top:0px;left:0px"></div>
							    </div>

							    <div class="col-2 room blue-door-color">Bathroom 4
						      		<div id="bath4dup1" class="droptarget">{bath4dup1}</div>
						      		<div class="standing-door blue-door-color" style="top:0px;right:0px"></div>
						    	</div>
						    	<div class="col-2">
						    	</div>


							</div>
						</div>

						<div class="col-12">
							<div class="row">
	

							    <div class="col-3 room red-door-color">Kitchen 1
						      		<div id="kitchen1dup1" class="droptarget">{kitchen1dup1}</div>
						      		<div class="standing-door red-door-color" style="bottom:0px;left:0px"></div>
						    	</div>


								 <div class="col-3 room blue-door-color">Laundry 1
							      	<div id="laundry1dup1" class="droptarget">{laundry1dup1}</div>
							      	<div class="standing-door blue-door-color" style="top:0px;left:0px"></div>
							    </div>

							    <div class="col-3 room blue-door-color">Laundry 2
							      	<div id="laundry2dup1" class="droptarget">{laundry2dup1}</div>
							      	<div class="standing-door blue-door-color" style="top:0px;right:0px"></div>
							    </div>

							    <div class="col-3 room red-door-color">Kitchen 2
						      		<div id="kitchen2dup1" class="droptarget">{kitchen2dup1}</div>
						      		<div class="standing-door red-door-color" style="bottom:0px;right:0px"></div>
						    	</div>


							</div>
						</div>

						<div class="col-12">
							<div class="row">
	

							    <div class="col-3 room red-door-color">Dining 1
						      		<div id="dining1dup1" class="droptarget">{dining1dup1}</div>
						    	</div>


								 <div class="col-3 room orange-door-color">Living 1
							      	<div id="living1dup1" class="droptarget">{living1dup1}</div>
							      	<div class="sleeping-door orange-door-color" style="bottom:0px;left:0px"></div>
							    </div>

							    <div class="col-3 room orange-door-color">Living 2
							      	<div id="living2dup1" class="droptarget">{living2dup1}</div>
							      	<div class="sleeping-door orange-door-color" style="bottom:0px;right:0px"></div>
							    </div>

							    <div class="col-3 room red-door-color">Dining 2
						      		<div id="dining2dup1" class="droptarget">{dining2dup1}</div>
						    	</div>

							</div>
						</div>

						<div class="col-12">
							<div class="row">
	

							    <div class="col-2">
						      		
						    	</div>


								 <div class="col-4 room orange-door-color">Porch 1
							      	<div id="porch1dup1" class="droptarget">{porch1dup1}</div>
							    </div>

							    <div class="col-4 room orange-door-color">Porch 2
							      	<div id="porch2dup1" class="droptarget">{porch2dup1}</div>
							    </div>

							    <div class="col-2">
						      		
						    	</div>

							</div>
						</div>





				
				  </div>
				"""

			if(simulation_id == '90'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {

					'kitchen1tg': 'kitchen1tg',
					'kitchen2tg': 'kitchen2tg',
					'kitchen3tg': 'kitchen3tg',

					'tb1tg': 'tb1tg',
					'tb2tg': 'tb2tg',
					'tb3tg': 'tb3tg',

					'dining1tg': 'dining1tg',
					'dining2tg': 'dining2tg',
					'dining3tg': 'dining3tg',

					'living1tg': 'living1tg',
					'living2tg': 'living2tg',
					'living3tg': 'living3tg'


				}
				result = """
				<div class="row mt-3">


						<div class="col-12">
							<div class="row">
	

							    <div class="col-1">
						      		
						    	</div>

								<div class="col-2 room red-door-color">Kitchen 1
						      		<div id="kitchen1tg" class="droptarget">{kitchen1tg}</div>
						      		
						    	</div>

								<div class="col-1 room blue-door-color">Bathroom
						      		<div id="tb1tg" class="droptarget">{tb1tg}</div>
						      		<div class="standing-door blue-door-color" style="bottom:0px;left:0px"></div>
						      		
						    	</div>

						   		<div class="col-1">
						      		
						    	</div>

								<div class="col-2 room red-door-color">Kitchen 2
						      		<div id="kitchen2tg" class="droptarget">{kitchen2tg}</div>
						      		
						    	</div>

								<div class="col-1 room blue-door-color">Bathroom
						      		<div id="tb2tg" class="droptarget">{tb2tg}</div>
						      		<div class="standing-door blue-door-color" style="bottom:0px;left:0px"></div>
						      		
						    	</div>

						    	<div class="col-1">
						      		
						    	</div>

								<div class="col-2 room red-door-color">Kitchen 3
						      		<div id="kitchen3tg" class="droptarget">{kitchen3tg}</div>
						      		
						    	</div>

								<div class="col-1 room blue-door-color">Bathroom
						      		<div id="tb3tg" class="droptarget">{tb3tg}</div>
						      		<div class="standing-door blue-door-color" style="bottom:0px;left:0px"></div>
						      		
						    	</div>

							</div>
						</div>


						<div class="col-12">
							<div class="row">
	

								<div class="col-4 room  red-door-color">Dining 1
							      	<div id="dining1tg" class="droptarget">{dining1tg}</div>
							    </div>

							    <div class="col-4 room  red-door-color">Dining 2
							      	<div id="dining2tg" class="droptarget">{dining2tg}</div>
							    </div>

							     <div class="col-4 room  red-door-color">Dining 3
							      	<div id="dining3tg" class="droptarget">{dining3tg}</div>
							    </div>


							</div>
						</div>

						<div class="col-12">
							<div class="row">
	

								<div class="col-4 room  orange-door-color">Living 1
							      	<div id="living1tg" class="droptarget">{living1tg}</div>
							      	<div class="sleeping-door orange-door-color" style="bottom:0px;right:0px"></div>

							    </div>

							    <div class="col-4 room orange-door-color">Living 2
							      	<div id="living2tg" class="droptarget">{living2tg}</div>
							      	<div class="sleeping-door orange-door-color" style="bottom:0px;right:0px"></div>

							    </div>

							     <div class="col-4 room orange-door-color">Living 3
							      	<div id="living3tg" class="droptarget">{living3tg}</div>
							      	<div class="sleeping-door orange-door-color" style="bottom:0px;right:0px"></div>
							    </div>


							</div>
						</div>

				  </div>
				"""




			if(simulation_id == '91'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {

					'dinnerkitchenB2': 'dinnerkitchenB2',
					'bathB2': 'bathB2',
					'bed1B2': 'bed1B2',
					'livingB2': 'livingB2',
					'bed2B2': 'bed2B2',
					'bed3B2': 'bed3B2'




				}
				result = """
				<div class="row mt-3" style="max-width:650px;margin:auto">


						<div class="col-12">
							<div class="row">
	

								<div class="col-4 room red-door-color" style="height:170px">Dining / Kitchen<br><br><br>
							      	<div id="dinnerkitchenB2" class="droptarget">{dinnerkitchenB2}</div>
							      	<div class="sleeping-door red-door-color" style="bottom:0px;left:0px"></div>
							    </div>

							    <div class="col-4 room blue-door-color" style="height:170px">Bathroom<br><br><br>
							      	<div id="bathB2" class="droptarget">{bathB2}</div>
							      	<div class="sleeping-door blue-door-color" style="bottom:0px;left:0px"></div>

							    </div>

							     <div class="col-4 room yellow-door-color align-self-end" style="height:170px">Bedroom 1<br><br><br>
							      	<div id="bed1B2" class="droptarget">{bed1B2}</div>
							      	<div class="sleeping-door yellow-door-color" style="bottom:0px;left:0px"></div>

							     
							    </div>

   								 <div class="col-8 room orange-door-color"style="height:170px">Living Room<br><br><br>
							      	<div id="livingB2" class="droptarget">{livingB2}</div>
							      		<div class="standing-door orange-door-color" style="bottom:60px;right:0px"></div>

							    </div>


  								 <div class="col-4 room yellow-door-color" style="height:170px">Bedroom 3<br><br><br>
  								 <div  id="bed3B2" class="droptarget">{bed3B2}</div>
  								
							    </div>


							     <div class="col-6 room align-self-end yellow-door-color" style="height:170px">Bedroom 2<br><br><br>
							      	<div id="bed2B2" class="droptarget">{bed2B2}</div>
							      	<div class="sleeping-door yellow-door-color" style="top:0px;right:0px"></div>
							     
							    </div>


							     <div class="col-6 room align-self-end yellow-door-color" style="height:170px"><br><br><br><br>
							      	<div style="visibility:hidden" id="bed3B2" class="droptarget">{bed3B2}</div>
							     
							    </div>




							</div>
						</div>


				  </div>
				"""

			if(simulation_id == '92'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {

					'masterbedB3': 'masterbedB3',
					'masterbathB3': 'masterbathB3',
					'bathB3': 'bathB3',
					'bedB3': 'bedB3',

					'closetB3': 'closetB3',
					'laundryB3': 'laundryB3',
					'bed2B3': 'bed2B3',

					'deckB3': 'deckB3',
					'diningB3': 'diningB3',
					'livingB3': 'livingB3',

					'kitchenB3': 'kitchenB3',
					'coverporchB3': 'coverporchB3',


				}
				result = """
				<div class="row mt-3" style="max-width:1000px;margin:auto">
						<div class="col-12">

								<div class="row">
	
										<div class="col-4 room yellow-door-color">Master Bedroom
									      	<div id="masterbedB3" class="droptarget">{masterbedB3}</div>
									      	<div class="sleeping-door yellow-door-color" style="bottom:0px;right:0px"></div>
									      	
									    </div>

									    <div class="col-2 room blue-door-color">Master Bath
									      	<div id="masterbathB3" class="droptarget">{masterbathB3}</div>
									      	<div class="standing-door blue-door-color" style="bottom:0px;left:0px"></div>

									    </div>

									    <div class="col-2 room blue-door-color">Bath
									      	<div id="bathB3" class="droptarget">{bathB3}</div>
									     <div class="standing-door blue-door-color" style="bottom:0px;right:0px"></div>
									    </div>


										<div class="col-4 room yellow-door-color">Bedroom 1
									      	<div id="bedB3" class="droptarget">{bedB3}</div>
									      	<div class="sleeping-door yellow-door-color" style="bottom:0px;left:0px"></div>
									      	
									    </div>

							        </div>


							    <div class="row">

								    <div class="col-3 room yellow-door-color">Walk-in Closet
								      	<div id="closetB3" class="droptarget">{closetB3}</div>
								      	<div class="sleeping-door yellow-door-colo"  style="top:0px;right:0px"></div>

								    </div>

								    <div class="col-3 room blue-door-color">Laundry
								      	<div id="laundryB3" class="droptarget">{laundryB3}</div>
								      	<div class="sleeping-door blue-door-color" style="bottom:0px;right:0px"></div>
								    </div>
								    <div class="col-2">
								      
								    </div>

								    <div class="col-4 room yellow-door-color">Bedroom 2
								      	<div id="bed2B3" class="droptarget">{bed2B3}</div>
								      	<div class="standing-door yellow-door-color" style="bottom:0px;left:0px"></div>
								    </div>

							    </div>

							    <div class="row">

								    <div class="col-2 room orange-door-color">Deck
								      	<div id="deckB3" class="droptarget">{deckB3}</div>
								      
								    </div>

								    <div class="col-5 red yellow-door-color">Dining Room
								      	<div id="diningB3" class="droptarget">{diningB3}</div>
								      
								    </div>

								    <div class="col-5 room orange-door-color">Living Room
								      	<div id="livingB3" class="droptarget">{livingB3}</div>
								      	<div class="sleeping-door orange-door-color" style="bottom:0px;left:0px"></div>
								    </div>

							    </div>


							<div class="row">
								     <div class="col-2">
								      
								    </div>

								     <div class="col-5 room red-door-color">Kitchen
								      	<div id="kitchenB3" class="droptarget">{kitchenB3}</div>
								    </div>

								    <div class="col-5 room orange-door-color">Covered Porch
								      	<div id="coverporchB3" class="droptarget">{coverporchB3}</div>
								      		<div class="sleeping-door orange-door-color" style="bottom:0px;left:0px"></div>
								    </div>
							</div>



						</div>
				  </div>
				"""

			# Fill in the placeholders with images
			for html_id, room_id in room_id_map.items():
			    images_html = ""
			    if room_id in grouped_data:
			        images_html = "".join(
			            f''' <div> 
			                    <div data-bs-toggle="modal" data-bs-target="#appModal" data-input-hr="{canvas_id}_{watt}_{applianceName}_{grouped_data[room_id]['roomName']}">
			                        <input type="hidden" id="{canvas_id}_{watt}_{applianceName}_{grouped_data[room_id]['roomName']}" class="toggleInput" value="1">
			                        <img data-bs-toggle="tooltip" data-bs-placement="top" title="{applianceName} - {watt} W " draggable="true" data-is-update="1" data-canvas-id="{canvas_id}" 
			                        data-custom-id="{room_id}" id="{image_id}" src="assets/uploads/{image}" style="height:30px;"  />
			                    </div>
			                </div>'''
			            for image, image_id, canvas_id, watt, applianceName in grouped_data[room_id]['images']
			        )
			    result = result.replace(f'{{{html_id}}}', images_html)

			# Replace any remaining placeholders with empty strings
			for html_id in room_id_map.keys():
				result = result.replace(f'{{{html_id}}}', '')

			return {'message': result}
		except sqlite3.Error as e:
			print(f"An error occurred: {e}")
		finally:
			if connection:
				connection.close()


	# def fetch_room(self, simulation_id):
	#     try:
	#         # Connect to the SQLite database
	#         connection = sqlite3.connect('ecoenergy.db')
	#         cursor = connection.cursor()
			
	#         # Query to fetch room and canvas details
	#         query = """SELECT room.id AS roomId, room.name AS roomName, sub_appliance.image AS applianceImage, 
	#         sub_appliance.id AS applianceImageId, simulation.*, canvas.id AS canvasRow
	#         FROM canvas 
	#         INNER JOIN room ON room.id = canvas.room_id
	#         INNER JOIN sub_appliance ON sub_appliance.id = canvas.appliance_id
	#         INNER JOIN simulation ON simulation.id = canvas.simulation_id 
	#         WHERE canvas.simulation_id = ?;"""
	#         cursor.execute(query, (simulation_id,))
	#         rows = cursor.fetchall()  # Fetch all rows from the query result

	#         columns = [description[0] for description in cursor.description]  # Get column names

	#         # Fetch all rooms
	#         query_rooms = """SELECT room.id AS roomId, room.name AS roomName FROM room
	#                          WHERE room.simulation_id = ?;"""
	#         cursor.execute(query_rooms, (simulation_id,))
	#         rooms = cursor.fetchall()

	#         # Group images by roomId
	#         grouped_data = {}
	#         for row in rows:
	#             row_data = {columns[i]: row[i] for i in range(len(row))}
	#             room_id = row_data['roomId']
	#             canvas_id = row_data['canvasRow']  # Fetch the canvas.id
				
	#             if room_id not in grouped_data:
	#                 grouped_data[room_id] = {
	#                     'roomName': row_data['roomName'],
	#                     'canvasRow': canvas_id,
	#                     'images': []
	#                 }
	#             # Append image, image_id, and canvas_id to the list of images
	#             grouped_data[room_id]['images'].append((row_data['applianceImage'], row_data['applianceImageId'], canvas_id))

	#         # Generate HTML
	#         result = ""
	#         for room in rooms:
	#             room_id = room[0]
	#             room_name = room[1]
	#             images_html = ""
	#             if room_id in grouped_data:
	#                 images_html = "".join(
	#                     f'<img draggable="true" data-is-update="1" data-canvas-id="{canvas_id}" data-custom-id="{room_id}" id="{image_id}" src="assets/uploads/{image}" style="width:60px; height:60px;" />' 
	#                     for image, image_id, canvas_id in grouped_data[room_id]['images']
	#                 )
	#             result += f"""<div class="col-3">
	#                             {room_name}
	#                             <div class="droptarget" id="{room_id}">
	#                                 {images_html}
	#                             </div>
	#                         </div>"""

	#         return {'message': result}
		
	#     except sqlite3.Error as e:
	#         return {'error': f"Error: {e}"}
	#     finally:
	#         cursor.close()
	#         connection.close()


	def get_suggestions(self, target_bill, target_hours, rate_per_hr, simulation_id):
	    try:
	        # Connect to the SQLite database
	        connection = sqlite3.connect('ecoenergy.db')
	        cursor = connection.cursor()

	        # Calculate target watt-hours based on the bill
	        rate_per_kwh =  float(rate_per_hr)  # PESO per kilowatt-hour
	        target_wh = (float(target_bill) / rate_per_kwh) * 1000  # Convert bill to watt-hours

	        # Query to get appliance data filtered by simulation_id
	        query = '''
	            SELECT canvas.id, canvas.room_id, canvas.appliance_id, sub_appliance.watt, sub_appliance.name 
	            FROM canvas
	            JOIN sub_appliance ON canvas.appliance_id = sub_appliance.id
	            WHERE canvas.simulation_id = ?
	        '''
	        cursor.execute(query, (simulation_id,))
	        rows = cursor.fetchall()
	        
	        # Start building the HTML output for the scrollable column
	        html_output = '''
	            <div class="container">
	                <div class="row">
	        '''

	        current_room_id = None
	        total_wh_consumption = 0
	        room_wh_consumption = 0
	        room_bill = 0

	        room_data = {}

	        # Calculate the total watts for all appliances
	        total_wattage = sum(float(row[3]) for row in rows if row[3])

	        for row in rows:
	            room_id, appliance_id, watt, appliance_name = row[1], row[2], row[3], row[4]
	            watt = float(watt) if watt else 0

	            # Calculate suggested hours based on the total wattage
	            if total_wattage > 0:
	                suggested_hours = (target_wh / total_wattage)
	            else:
	                suggested_hours = 0

	            # Calculate watt-hours and bill for the appliance
	            appliance_wh = watt * suggested_hours
	            appliance_bill = (appliance_wh / 1000) * rate_per_kwh

	            # Accumulate total consumption and bill
	            total_wh_consumption += appliance_wh

	            if room_id not in room_data:
	                room_query = 'SELECT name FROM room WHERE id = ?'
	                cursor.execute(room_query, (room_id,))
	                room_name = cursor.fetchone()
	                room_name = room_name[0] if room_name else "Unknown Room"
	                room_data[room_id] = {
	                    'room_name': room_name,
	                    'appliances': [],
	                    'room_wh_consumption': 0,
	                    'room_bill': 0
	                }

	            room_data[room_id]['appliances'].append({
	                'appliance_name': appliance_name,
	                'suggested_hours': suggested_hours,
	                'appliance_bill': appliance_bill
	            })
	            room_data[room_id]['room_wh_consumption'] += appliance_wh
	            room_data[room_id]['room_bill'] += appliance_bill

	        for room_id, room in room_data.items():
	            html_output += f'''
	                <div class="col-md-12 border room-section mb-3" style="height:auto">
	                    <p class="text-primary">{room['room_name']}</p>
	                    <div class="appliance-list" style="height:auto">
	            '''
	            for appliance in room['appliances']:
	                html_output += f'''
	                    <div class="appliance" style="height:auto">
	                        <span>Appliance: {appliance['appliance_name']}</span><br>
	                        <span>Suggested Usage: {appliance['suggested_hours']:.2f} hours</span><br>
	                        <span>Appliance Bill: {appliance['appliance_bill']:.2f} PESO</span>
	                        <hr style="width:auto">
	                    </div>
	                '''
	            html_output += f'''
	                    </div>
	                    <div class="room-total-bill">
	                        <p>Total Room Bill: {room['room_bill']:.2f} PESO</p>
	                    </div>
	                </div>
	            '''

	        # Calculate the total bill based on the total watt-hours consumed
	        total_bill = (total_wh_consumption / 1000) * rate_per_kwh

	        # Append the total bill to the HTML output
	        html_output += f'''
	            <div class="col-12 total-bill">
	                <p>Total Estimated Bill: {total_bill:.2f} PESO</p>
	            </div>
	        '''

	        # Close the main row and container divs
	        html_output += '</div></div>'

	        return {'message': html_output}

	    except Exception as e:
	        print(f"Error occurred: {e}")
	        return {'message': '<p>An error occurred while fetching suggestions.</p>'}

	    finally:
	        cursor.close()
	        connection.close()



	def get_suggestions_energy(self, target_kwh, rate_per_hr, simulation_id):
	    try:
	        # Connect to the SQLite database
	        connection = sqlite3.connect('ecoenergy.db')
	        cursor = connection.cursor()

	        # Calculate target watt-hours based on the kWh input
	        target_wh = float(target_kwh) * 1000  # Convert kWh to watt-hours

	        # Query to get appliance data filtered by simulation_id
	        query = '''
	            SELECT canvas.id, canvas.room_id, canvas.appliance_id, sub_appliance.watt, sub_appliance.name 
	            FROM canvas
	            JOIN sub_appliance ON canvas.appliance_id = sub_appliance.id
	            WHERE canvas.simulation_id = ?
	        '''
	        cursor.execute(query, (simulation_id,))
	        rows = cursor.fetchall()
	        
	        # Start building the HTML output for the scrollable column
	        html_output = '''
	            <div class="container">
	                <div class="row">
	        '''

	        current_room_id = None
	        total_wh_consumption = 0
	        room_wh_consumption = 0
	        room_bill = 0

	        room_data = {}

	        # Calculate the total watts for all appliances
	        total_wattage = sum(float(row[3]) for row in rows if row[3])

	        for row in rows:
	            room_id, appliance_id, watt, appliance_name = row[1], row[2], row[3], row[4]
	            watt = float(watt) if watt else 0

	            # Calculate suggested hours based on the total wattage
	            if total_wattage > 0:
	                suggested_hours = (target_wh / total_wattage)
	            else:
	                suggested_hours = 0

	            # Calculate watt-hours and bill for the appliance
	            appliance_wh = watt * suggested_hours
	            rate_per_kwh =  float(rate_per_hr)  # PESO per kilowatt-hour
	            appliance_bill = (appliance_wh / 1000) * rate_per_kwh

	            # Accumulate total consumption and bill
	            total_wh_consumption += appliance_wh

	            if room_id not in room_data:
	                room_query = 'SELECT name FROM room WHERE id = ?'
	                cursor.execute(room_query, (room_id,))
	                room_name = cursor.fetchone()
	                room_name = room_name[0] if room_name else "Unknown Room"
	                room_data[room_id] = {
	                    'room_name': room_name,
	                    'appliances': [],
	                    'room_wh_consumption': 0,
	                    'room_bill': 0
	                }

	            room_data[room_id]['appliances'].append({
	                'appliance_name': appliance_name,
	                'suggested_hours': suggested_hours,
	                'appliance_bill': appliance_bill
	            })
	            room_data[room_id]['room_wh_consumption'] += appliance_wh
	            room_data[room_id]['room_bill'] += appliance_bill

	        for room_id, room in room_data.items():
	            html_output += f'''
	                <div class="col-md-12 border room-section mb-3" style="height:auto">
	                    <p class="text-primary">{room['room_name']}</p>
	                    <div class="appliance-list" style="height:auto">
	            '''
	            for appliance in room['appliances']:
	                html_output += f'''
	                    <div class="appliance" style="height:auto">
	                        <span>Appliance: {appliance['appliance_name']}</span><br>
	                        <span>Suggested Usage: {appliance['suggested_hours']:.2f} hours</span><br>
	                        <span>Appliance Bill: {appliance['appliance_bill']:.2f} PESO</span>
	                        <hr style="width:auto">
	                    </div>
	                '''
	            html_output += f'''
	                    </div>
	                    <div class="room-total-bill">
	                        <p>Total Room Bill: {room['room_bill']:.2f} PESO</p>
	                    </div>
	                </div>
	            '''

	        # Calculate the total bill based on the total watt-hours consumed
	        total_bill = (total_wh_consumption / 1000) * rate_per_kwh

	        # Append the total bill to the HTML output
	        html_output += f'''
	            <div class="col-12 total-bill">
	                <p>Total Estimated Bill: {total_bill:.2f} PESO</p>
	            </div>
	        '''

	        # Close the main row and container divs
	        html_output += '</div></div>'

	        return {'message': html_output}

	    except Exception as e:
	        print(f"Error occurred: {e}")
	        return {'message': '<p>An error occurred while fetching suggestions.</p>'}

	    finally:
	        cursor.close()
	        connection.close()






	
	def fetch_data(self):
		try:
			# Connect to the SQLite database (it will create the file if it doesn't exist)
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()
			
			# Execute the query
			cursor.execute("SELECT * FROM users;")
			rows = cursor.fetchall()  # Fetch all rows from the query result
			columns = [description[0] for description in cursor.description]  # Get column names

			# Return the fetched data as a string (for simplicity)
			result = ""
			for row in rows:
				row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
				result += f"""<tr>
								<td>{row_data['id']}</td>
								<td>{row_data['firstname']}</td>
								<td>{row_data['lastname']}</td>
							</tr>"""
	  
			return {'message': result}
		
		except sqlite3.Error as e:
			return {'message': f"Error: {e}"}
		finally:
			cursor.close()
			connection.close()

	def search_data(self, searchByName):
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect('ecoenergy.db')
			cursor = connection.cursor()

			# Query to search name
			query = "SELECT * FROM users WHERE firstname LIKE ? OR lastname LIKE ?;"
			search_pattern = f"%{searchByName}%"  # Add wildcard characters before and after the search term
			cursor.execute(query, (search_pattern, search_pattern))

			rows = cursor.fetchall()  # Fetch all rows from the query result
			columns = [description[0] for description in cursor.description]  # Get column names
			result = ""
			if not rows:
				result += f"""<tr>
								<td style="text-align:center" colspan="3">No data found</td>
							  </tr>"""
			else:
				# Return the fetched data as a string (for simplicity)
				for row in rows:
					row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
					result += f"""<tr>
									<td>{row_data['id']}</td>
									<td>{row_data['firstname']}</td>
									<td>{row_data['lastname']}</td>
								</tr>"""
			
			return {'message': result}
		
		except sqlite3.Error as e:
			return {'message': f"Error: {e}"}
		finally:
			cursor.close()
			connection.close()


def on_loaded():
	window.toggle_fullscreen()


if __name__ == '__main__':
	api = Api()
	
	# Get the path to the HTML file
	current_dir = os.path.dirname(os.path.realpath(__file__))
	html_path = os.path.join(current_dir, 'index.html')

	# Create the window using the external HTML file
	window = webview.create_window('ECO ENEGERY', html_path, js_api=api, width=1000, height=700,)
	webview.start()
