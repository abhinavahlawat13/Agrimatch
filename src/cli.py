from engine import Agrimatch
def get_user_input():
     features = [
      ("Nitrogen (N)", 0, 300),
      ("Phosphorus (P)", 0, 300),
      ("Potassium (K)", 0, 300),
      ("Temperature (°C)", -10, 60),
      ("Humidity (%)", 0, 100),
      ("pH", 0.0, 14.0),
      ("Rainfall (mm)", 0, 1000),
        ]
     inputs = []
     for feature_name, min_val, max_val in features:
         while True:
          user_input = input(f"enter {feature_name} value : ")
          try:
            value = float(user_input)

            if not min_val <= value <= max_val:
              print(
                  f"value must between {min_val} and {max_val} please try again"
                  " "
              )
              continue

            inputs.append(value)
            break
          except ValueError:
            print("Invalid input. Please enter a numeric value.")