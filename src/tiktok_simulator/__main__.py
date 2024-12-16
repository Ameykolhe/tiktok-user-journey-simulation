from tiktok_simulator.simulator import TikTokSimulator

if __name__ == '__main__':
    simulator = TikTokSimulator()

    simulator.init()

    simulator.run()

    input("Press Enter to continue...")
    simulator.teardown()
