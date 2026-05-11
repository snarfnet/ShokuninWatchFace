import CoreMotion
import Combine

final class MotionManager: ObservableObject {
    private let motion = CMMotionManager()

    @Published var pitch: Double = 0
    @Published var roll: Double = 0
    @Published var angle: Double = 0

    func startUpdates() {
        guard motion.isDeviceMotionAvailable else { return }
        motion.deviceMotionUpdateInterval = 1.0 / 30.0
        motion.startDeviceMotionUpdates(to: .main) { [weak self] data, _ in
            guard let self, let data else { return }
            self.pitch = data.attitude.pitch * 180 / .pi
            self.roll = data.attitude.roll * 180 / .pi
            self.angle = abs(self.pitch)
        }
    }

    func stopUpdates() {
        motion.stopDeviceMotionUpdates()
    }
}
