import webview
import os
import sqlite3
import base64
import uuid

# To browser
import threading
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  

class Api:

	# list of house
	def navbar(self):
		# Connect to the SQLite database (it will create the file if it doesn't exist)
		connection = sqlite3.connect('ecoenergy.db')
		cursor = connection.cursor()
			
		# Execute the query
		cursor.execute("SELECT * FROM simulation ORDER BY name;")
		rows = cursor.fetchall()  # Fetch all rows from the query result
		columns = [description[0] for description in cursor.description]  # Get column names

		# Return the fetched data as a string (for simplicity)
		simulations = ""

		for row in rows:
			row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
			simulations += f"""
				<li>
					<a href="#" 
					onclick="setID('{row_data['name']}', '{row_data['id']}');" 
					class="dropdown-item d-flex align-items-center py-2 px-3 hover-bg-gray-100">
						<i class="fas fa-home me-2"></i>
						<span class="text-dark">{row_data['name']}</span>
					</a>
				</li>
			"""

		r = f"""
			<div class="house-selector">
				<div class="dropdown">
					<button class="btn btn-outline-primary dropdown-toggle w-100" 
							type="button" 
							id="navbarDropdownMenuLink" 
							data-bs-toggle="dropdown" 
							aria-expanded="false">
						<i class="fas fa-home me-2"></i>
						Choose A Layout
					</button>
					<ul class="dropdown-menu w-100 shadow-sm border-0" 
						aria-labelledby="navbarDropdownMenuLink">
						{simulations}
					</ul>
				</div>
			</div>
		"""
		
		return {'message': r}

	# list of appliances 
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
					    <img data-bs-placement="top" title="{appliance_data['name']}" draggable="false" data-is-update="0" id="s{appliance_data['id']}" data-bs-toggle="dropdown" aria-expanded="false" src="assets/vectors/{appliance_data['image']}" />
    					<ul class="dropdown-menu" aria-labelledby="s{appliance_data['id']}">
						<div class="text-center">
				"""
				for sub_appliance in sub_appliances:
					sub_appliance_data = {sub_appliance_columns[i]: sub_appliance[i] for i in range(len(sub_appliance))}
					result += f"""
							<div>
								<img data-bs-toggle="tooltip" data-bs-placement="top" title="{sub_appliance_data['name']} - {sub_appliance_data['watt']} W" draggable="true" id="{sub_appliance_data['id']}" src="assets/uploads/{sub_appliance_data['image']}"/>
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

			if(simulation_id == '93'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'B1_bedTop': 'B1_bedTop',
					'B1_kitchen': 'B1_kitchen',
					'B1_bath': 'B1_bath',
					'B1_dining': 'B1_dining',
					'B1_bedBot': 'B1_bedBot',
					'B1_livingRoom': 'B1_livingRoom',
					'B1_porch': 'B1_porch',
				}
				result = """
					<div class="floor-plan" style="position: relative; width: 1000px; height: 800px; margin: auto;">

						<!-- Bedroom Top -->
						<div class="room" style="position: absolute; top: 212px; left: 320px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_bedTop" class="droptarget">{B1_bedTop}</div>
						</div>

						<!-- Kitchen -->
						<div class="room" style="position: absolute; top: 200px; left: 566px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_kitchen" class="droptarget">{B1_kitchen}</div>
						</div>

						<!-- Bath -->
						<div class="room" style="position: absolute; top: 385px; right: 576px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_bath" class="droptarget">{B1_bath}</div>
						</div>

						<!-- Dining -->
						<div class="room" style="position: absolute; top: 347px; left: 552px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_dining" class="droptarget">{B1_dining}</div>
						</div>

						<!-- Bedroom Bottom -->
						<div class="room" style="position: absolute; top: 547px; left: 320px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_bedBot" class="droptarget">{B1_bedBot}</div>
						</div>

						<!-- Living Room -->
						<div class="room" style="position: absolute; top: 506px; right: 286px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_livingRoom" class="droptarget">{B1_livingRoom}</div>
						</div>

						<!-- Porch -->
						<div class="room" style="position: absolute; top: 710px; right: 288px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B1_porch" class="droptarget">{B1_porch}</div>
						</div>

					
					</div>
				"""
			
			if(simulation_id == '94'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'B2_dining/kitchen': 'B2_dining/kitchen',
					'B2_bedTopLeft': 'B2_bedTopLeft',
					'B2_bedTopRight': 'B2_bedTopRight',
					'B2_livingRoom': 'B2_livingRoom',
					'B2_bathTop': 'B2_bathTop',
					'B2_bathBot': 'B2_bathBot',
					'B2_garage': 'B2_garage',
					'B2_porch': 'B2_porch',
					'B2_bedBot': 'B2_bedBot',
				}
				result = """
					<div class="floor-plan" style="position: relative; width: 1000px; height: 800px; margin: auto;">

						<!-- Kitchen -->
						<div class="room" style="position: absolute; top: 244px; left: 157px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_dining/kitchen" class="droptarget">{B2_dining/kitchen}</div>
						</div>

						<!-- Bedroom Top Left -->
						<div class="room" style="position: absolute; top: 188px; left: 367px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_bedTopLeft" class="droptarget">{B2_bedTopLeft}</div>
						</div>

						<!-- Bedroom Top Right -->
						<div class="room" style="position: absolute; top: 188px; left: 574px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_bedTopRight" class="droptarget">{B2_bedTopRight}</div>
						</div>

						<!-- Living Room -->
						<div class="room" style="position: absolute; top: 378px; left: 368px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_livingRoom" class="droptarget">{B2_livingRoom}</div>
						</div>

						<!-- Bath Top -->
						<div class="room" style="position: absolute; top: 338px; left: 644px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_bathTop" class="droptarget">{B2_bathTop}</div>
						</div>

						<!-- Bath Bottom -->
						<div class="room" style="position: absolute; top: 441px; left: 644px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_bathBot" class="droptarget">{B2_bathBot}</div>
						</div>

						<!-- Garage -->
						<div class="room" style="position: absolute; top: 523px; left: 151px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_garage" class="droptarget">{B2_garage}</div>
						</div>

						<!-- Porch -->
						<div class="room" style="position: absolute; top: 576px; left: 576px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_porch" class="droptarget">{B2_porch}</div>
						</div>

						<!-- Bedroom Bottom -->
						<div class="room" style="position: absolute; top: 630px; left: 364px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B2_bedBot" class="droptarget">{B2_bedBot}</div>
						</div>
					</div>
				"""
			
			if(simulation_id == '95'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'B3_kitchen': 'B3_kitchen',
					'B3_walkInCloset': 'B3_walkInCloset',
					'B3_dining': 'B3_dining',
					'B3_bedTop': 'B3_bedTop',
					'B3_garage': 'B3_garage',
					'B3_masterBedroom': 'B3_masterBedroom',
					'B3_livingRoom': 'B3_livingRoom',
					'B3_bathroom': 'B3_bathroom',
					'B3_porch': 'B3_porch',
					'B3_bedBot': 'B3_bedBot',
				}
				result = """
					<div class="floor-plan" style="position: relative; width: 1000px; height: 800px; margin: auto;">

						<!-- Kitchen -->
						<div class="room" style="position: absolute; top: 206px; left: 290px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_kitchen" class="droptarget">{B3_kitchen}</div>
						</div>

						<!-- Walk-in Closet -->
						<div class="room" style="position: absolute; top: 293px; left: 379px; width: 80px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_walkInCloset" class="droptarget">{B3_walkInCloset}</div>
						</div>

						<!-- Dining -->
						<div class="room" style="position: absolute; top: 281px; left: 499px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_dining" class="droptarget">{B3_dining}</div>
						</div>

						<!-- Bedroom Top -->
						<div class="room" style="position: absolute; top: 269px; left: 701px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_bedTop" class="droptarget">{B3_bedTop}</div>
						</div>

						<!-- Garage -->
						<div class="room" style="position: absolute; top: 503px; left: 42px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_garage" class="droptarget">{B3_garage}</div>
						</div>

						<!-- Master Bedroom -->
						<div class="room" style="position: absolute; top: 514px; left: 280px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_masterBedroom" class="droptarget">{B3_masterBedroom}</div>
						</div>

						<!-- Living Room -->
						<div class="room" style="position: absolute; top: 463px; left: 499px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_livingRoom" class="droptarget">{B3_livingRoom}</div>
						</div>

						<!-- Bathroom -->
						<div class="room" style="position: absolute; top: 430px; left: 747px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_bathroom" class="droptarget">{B3_bathroom}</div>
						</div>

						<!-- Porch -->
						<div class="room" style="position: absolute; top: 657px; left: 493px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_porch" class="droptarget">{B3_porch}</div>
						</div>

						<!-- Bedroom Bottom -->
						<div class="room" style="position: absolute; top: 580px; left: 704px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="B3_bedBot" class="droptarget">{B3_bedBot}</div>
						</div>
					</div>
				"""
			
			if(simulation_id == '96'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'C1_machine': 'C1_machine',
					'C1_mud': 'C1_mud',
					'C1_kitchen': 'C1_kitchen',
					'C1_bed#2': 'C1_bed#2',
					'C1_mainBath': 'C1_mainBath',
					'C1_walkInCloset': 'C1_walkInCloset',
					'C1_dining': 'C1_dining',
					'C1_bathRight': 'C1_bathRight',
					'C1_mainBed': 'C1_mainBed',
					'C1_living': 'C1_living',
					'C1_bed#3': 'C1_bed#3',
					'C1_coveredPorch': 'C1_coveredPorch',
				}
				result = """
					<div class="floor-plan" style="position: relative; width: 1000px; height: 800px; margin: auto;">

						<!-- Machine Room -->
						<div class="room" style="position: absolute; top: 177px; left: 120px; width: 120px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_machine" class="droptarget">{C1_machine}</div>
						</div>

						<!-- Mud Room -->
						<div class="room" style="position: absolute; top: 107px; left: 204px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_mud" class="droptarget">{C1_mud}</div>
						</div>

						<!-- Kitchen -->
						<div class="room" style="position: absolute; top: 91px; left: 439px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_kitchen" class="droptarget">{C1_kitchen}</div>
						</div>

						<!-- Bedroom #2 -->
						<div class="room" style="position: absolute; top: 117px; left: 719px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_bed#2" class="droptarget">{C1_bed#2}</div>
						</div>

						<!-- Main Bathroom -->
						<div class="room" style="position: absolute; top: 340px; left: 90px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_mainBath" class="droptarget">{C1_mainBath}</div>
						</div>

						<!-- Walk-in Closet -->
						<div class="room" style="position: absolute; top: 314px; left: 274px; width: 120px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_walkInCloset" class="droptarget">{C1_walkInCloset}</div>
						</div>

						<!-- Dining Room -->
						<div class="room" style="position: absolute; top: 300px; left: 464px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_dining" class="droptarget">{C1_dining}</div>
						</div>

						<!-- Bathroom Right -->
						<div class="room" style="position: absolute; top: 308px; left: 747px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_bathRight" class="droptarget">{C1_bathRight}</div>
						</div>

						<!-- Main Bedroom -->
						<div class="room" style="position: absolute; top: 462px; left: 163px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_mainBed" class="droptarget">{C1_mainBed}</div>
						</div>

						<!-- Living Room -->
						<div class="room" style="position: absolute; top: 479px; left: 474px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_living" class="droptarget">{C1_living}</div>
						</div>

						<!-- Bedroom #3 -->
						<div class="room" style="position: absolute; top: 505px; left: 730px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_bed#3" class="droptarget">{C1_bed#3}</div>
						</div>

						<!-- Covered Porch -->
						<div class="room" style="position: absolute; top: 720px; left: 484px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="C1_coveredPorch" class="droptarget">{C1_coveredPorch}</div>
						</div>
					</div>
				"""
			
			if(simulation_id == '99'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'D1_bed3': 'D1_bed3',
					'D1_bed2': 'D1_bed2',
					'D1_kitchen': 'D1_kitchen',
					'D1_dining': 'D1_dining',
					'D1_laundry': 'D1_laundry',
					'D1_bathTop': 'D1_bathTop',
					'D1_bed1': 'D1_bed1',
					'D1_bathBot': 'D1_bathBot',
					'D1_living': 'D1_living',
					'D1_porch': 'D1_machine',

				}
				result = """
					<div class="floor-plan" style="position: relative; width: 1000px; height: 800px; margin: auto;">

						<!-- Bedroom 3 -->
						<div class="room" style="position: absolute; top: 100px; left: 138px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_bed3" class="droptarget">{D1_bed3}</div>
						</div>

						<!-- Bedroom 2 -->
						<div class="room" style="position: absolute; top: 100px; left: 368px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_bed2" class="droptarget">{D1_bed2}</div>
						</div>

						<!-- Kitchen -->
						<div class="room" style="position: absolute; top: 131px; left: 609px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_kitchen" class="droptarget">{D1_kitchen}</div>
						</div>

						<!-- Dining -->
						<div class="room" style="position: absolute; top: 325px; left: 619px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_dining" class="droptarget">{D1_dining}</div>
						</div>

						<!-- Laundry -->
						<div class="room" style="position: absolute; top: 370px; left: 102px; width: 120px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_laundry" class="droptarget">{D1_laundry}</div>
						</div>

						<!-- Bath Top -->
						<div class="room" style="position: absolute; top: 490px; left: 374px; width: 120px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_bathTop" class="droptarget">{D1_bathTop}</div>
						</div>

						<!-- Bedroom 1 -->
						<div class="room" style="position: absolute; top: 640px; left: 148px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_bed1" class="droptarget">{D1_bed1}</div>
						</div>

						<!-- Bath Bottom -->
						<div class="room" style="position: absolute; top: 700px; left: 374px; width: 120px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_bathBot" class="droptarget">{D1_bathBot}</div>
						</div>

						<!-- Living Room -->
						<div class="room" style="position: absolute; top: 585px; left: 566px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_living" class="droptarget">{D1_living}</div>
						</div>

						<!-- Porch -->
						<div class="room" style="position: absolute; top: 499px; left: 804px; width: 120px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_porch" class="droptarget">{D1_porch}</div>
						</div>
					</div>
				"""
			
			if(simulation_id == '100'):
				# Map HTML IDs to room IDs Bungalow 1
				room_id_map = {
					'D1_bed3': 'D1_bed3',
					'D1_bed2': 'D1_bed2',
					'D1_kitchen': 'D1_kitchen',
					'D1_dining': 'D1_dining',
					'D1_laundry': 'D1_laundry',
					'D1_bathTop': 'D1_bathTop',
					'D1_bed1': 'D1_bed1',
					'D1_bathBot': 'D1_bathBot',
					'D1_living': 'D1_living',
					'D1_porch': 'D1_machine',

				}
				result = """
					<div class="floor-plan" style="position: relative; width: 1000px; height: 800px; margin: auto;">

						<!-- Bedroom 3 -->
						<div class="room" style="position: absolute; top: 100px; left: 138px; width: 160px; height: 40px;">
							<span class="room-name"></span>
							<div id="D1_bed3" class="droptarget">{D1_bed3}</div>
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

	# canvas functions
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
	

api = Api()

@app.route('/api/navbar')
def navbar():
    return jsonify(api.navbar())

@app.route('/api/appliance_list')
def appliance_list():
    return jsonify(api.appliance_list())

@app.route('/api/fetch_room')
def fetch_room():
	simulation_id = request.args.get("simulationId")
	return jsonify(api.fetch_room(simulation_id))

@app.route('/api/add_appliance_canvas', methods=['POST'])
def add_appliance_canvas():
    data = request.json  # Get JSON data from request
    session_id = data.get("sessionId")
    room_id = data.get("roomId")
    image_id = data.get("imageId")
    return jsonify(api.add_appliance_canvas(session_id, room_id, image_id)) 
	
# Serve HTML and static files
@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

# Expose PyWebView API through Flask
@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.json
    return jsonify({"message": api.create_room(data['room'], data['simulationId'])})

@app.route('/api/get_suggestions_energy', methods=['POST'])
def get_suggestions_energy():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
    target_kwh = data.get('target_kwh')
    rate_per_hour = data.get('rate_per_hour')
    session_id = data.get('session_id')
    
    if not all([target_kwh, rate_per_hour, session_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
        
    return jsonify(api.get_suggestions_energy(target_kwh, rate_per_hour, session_id))

@app.route('/api/get_suggestions', methods=['POST'])
def get_suggestions():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
    target_amount = data.get('target_amount')
    target_hours = data.get('target_hours')
    rate_per_hour = data.get('rate_per_hour')
    session_id = data.get('session_id')
    
    if not all([target_amount, target_hours, rate_per_hour, session_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
        
    return jsonify(api.get_suggestions(target_amount, target_hours, rate_per_hour, session_id))

@app.route('/api/update_appliance_canvas', methods=['POST'])
def update_appliance_canvas():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
    session_id = data.get('session_id')
    room_id = data.get('room_id')
    image_id = data.get('image_id')
    from_room = data.get('from_room')
    canvas_id = data.get('canvas_id')
    
    if not all([session_id, room_id, image_id, from_room, canvas_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
        
    return jsonify(api.update_appliance_canvas(session_id, room_id, image_id, from_room, canvas_id))	

@app.route('/api/delete_appliance_canvas', methods=['POST'])
def delete_appliance_canvas():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
    canvas_id = data.get('canvas_id')
    if not canvas_id:
        return jsonify({'error': 'Missing canvas_id parameter'}), 400
        
    return jsonify(api.delete_appliance_canvas(canvas_id))

if __name__ == '__main__':
    # Start Flask server in a separate thread
    threading.Thread(target=lambda: app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False), daemon=True).start()
    
    # Open with the Flask server URL
    window = webview.create_window('ECO ENERGY', 'http://127.0.0.1:5000', js_api=api)
    webview.start()

