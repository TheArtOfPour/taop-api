class Stats:

    def __init__(self):
        print("init stats")

    def stats(self, data):
        print(data)

        return []

    def recipe_to_inputs(self, recipe):
        # convert to 6 inputs
        # 1 - y 1 hot
        # 2 - h 1 hot
        # 3 - ha (-1 to 1)
        # 4 - ht (-1 to 1)
        # 5 - f 1 hot
        # 6 - fa (-1 to 1)

        # c.execute("select MAX(id) AS max_id from yeast")
        # max_yeast = c.fetchone()[0] + 1
        # c.execute("select MAX(id) AS max_id from hops")
        # max_hop = c.fetchone()[0] + 1
        # c.execute("select MAX(id) AS max_id from fermentables")
        # max_fermentable = c.fetchone()[0] + 1
        # @TODO : detect and tolerate(normalize) indeterminate input shapes
        max_yeast = 15
        max_hop = 39
        max_fermentable = 40

        yeast = int(recipe['yeast'])
        hops = recipe['hops']
        fermentables = recipe['fermentables']

        one_hot_yeast = keras.utils.to_categorical(yeast, num_classes=max_yeast)[0]
        # @TODO : only log in debug mode
        print(one_hot_yeast)
        print("----------------------------")
        one_hot_hops = []
        hop_amounts = []
        hop_times = []
        count = 0
        print(str(len(hops)) + ' hops...')
        for hop in hops:
            count = count + 1
            # hop amount in ounces 0:36 -> -1:1
            amount = float("{:.3f}".format(float(hop['amount'])))
            hop_amount = ((amount / 36) * 2) - 1
            # hop time in minutes 0:90 -> -1:1
            hop_time = ((int(hop['time']) / 90) * 2) - 1
            # hop id in max_hop categories
            hop_id_hot = keras.utils.to_categorical(int(hop['id']), num_classes=max_hop)[0]
            hop_id_hot = numpy.delete(hop_id_hot, 0)
            hop_amounts.append(hop_amount)
            hop_times.append(hop_time)
            one_hot_hops.append(hop_id_hot)
        print(one_hot_hops)
        print("----------------------------")
        print('complete \n')

        one_hot_fermentables = []
        fermentable_amounts = []
        count = 0
        print(str(len(fermentables)) + ' fermentables...')
        for fermentable in fermentables:
            count = count + 1
            # fermentable amount in lbs 0:20 -> -1:1
            amount = float("{:.3f}".format(float(fermentable['amount'])))
            fermentable_amount = ((amount / 20) * 2) - 1
            # hop id in max_hop categories
            fermentable_id_hot = keras.utils.to_categorical(int(fermentable['id']), num_classes=max_fermentable)[0]
            fermentable_id_hot = numpy.delete(fermentable_id_hot, 0)
            fermentable_amounts.append(fermentable_amount)
            one_hot_fermentables.append(fermentable_id_hot)
        print(one_hot_fermentables)
        print("----------------------------")
        print('complete \n')

        one_hot_yeast = numpy.array([one_hot_yeast])
        one_hot_hops = numpy.array([one_hot_hops])
        hop_amounts = numpy.array([hop_amounts])
        hop_times = numpy.array([hop_times])
        one_hot_fermentables = numpy.array([one_hot_fermentables])
        fermentable_amounts = numpy.array([fermentable_amounts])
        # inputs = [one_hot_yeast, one_hot_hops, hop_amounts, hop_times, one_hot_fermentables, fermentable_amounts]
        inputs = [one_hot_yeast, one_hot_hops, one_hot_fermentables]
        return inputs
