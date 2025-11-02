from app import get_crop_recommendation

def test_crop_recommendation():
    # Test case 1: Sandy soil with low rainfall (drought conditions)
    print("\nTest Case 1: Sandy soil, low rainfall (drought conditions)")
    print("-" * 60)
    result = get_crop_recommendation(
        soil_type="sandy",
        ph_level=6.5,
        rainfall=250,  # Low rainfall
        temperature=32
    )
    print("Recommended crops:")
    for i, crop in enumerate(result, 1):
        print(f"{i}. {crop['name']} - {crop.get('description', 'No description')}")

    # Test case 2: Loamy soil with moderate rainfall
    print("\nTest Case 2: Loamy soil, moderate rainfall")
    print("-" * 60)
    result = get_crop_recommendation(
        soil_type="loamy",
        ph_level=7.0,
        rainfall=500,  # Moderate rainfall
        temperature=28
    )
    print("Recommended crops:")
    for i, crop in enumerate(result, 1):
        print(f"{i}. {crop['name']} - {crop.get('description', 'No description')}")

    # Test case 3: Black cotton soil with good rainfall
    print("\nTest Case 3: Black cotton soil, good rainfall")
    print("-" * 60)
    result = get_crop_recommendation(
        soil_type="black cotton",
        ph_level=7.2,
        rainfall=700,  # Good rainfall
        temperature=26
    )
    print("Recommended crops:")
    for i, crop in enumerate(result, 1):
        print(f"{i}. {crop['name']} - {crop.get('description', 'No description')}")

if __name__ == "__main__":
    test_crop_recommendation()
