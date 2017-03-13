def jars_content(jars, bell_peppers, cauliflowers, carrots, celeries):
    amounts = [bell_peppers, cauliflowers, celeries, carrots]
    veggies = ('bell_pepper', 'cauliflower', 'celery', 'carrot')
    crate = [[] for jar in range(jars)]

    while amounts != [0, 0, 0, 0] and jars > 0:
        for jar in range(len(crate)):
            for veggie, amount in enumerate(amounts):
                if amount >= (veggie + 1):
                    crate[jar].extend([veggies[veggie]] * (veggie + 1))
                    amounts[veggie] -= (veggie + 1)
                else:
                    crate[jar].extend([veggies[veggie]] * amount)
                    amounts[veggie] = 0

    return [iter(jar) for jar in crate]