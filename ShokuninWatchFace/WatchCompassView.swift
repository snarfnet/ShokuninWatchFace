import SwiftUI

struct WatchCompassView: View {
    @StateObject private var motion = MotionManager()

    var body: some View {
        VStack(spacing: 8) {
            Text("傾斜計")
                .font(.system(size: 16, weight: .black, design: .rounded))
                .foregroundStyle(WatchPalette.title)

            ZStack {
                Circle()
                    .fill(Color.black.opacity(0.44))
                    .overlay(Circle().stroke(WatchPalette.steel.opacity(0.35), lineWidth: 2))

                ForEach(0..<24, id: \.self) { index in
                    Rectangle()
                        .fill(index % 6 == 0 ? WatchPalette.amber : WatchPalette.steel.opacity(0.32))
                        .frame(width: index % 6 == 0 ? 2 : 1, height: index % 6 == 0 ? 10 : 5)
                        .offset(y: -58)
                        .rotationEffect(.degrees(Double(index) * 15))
                }

                VStack(spacing: 4) {
                    HStack(spacing: 16) {
                        VStack(spacing: 2) {
                            Text("PITCH")
                                .font(.system(size: 7, weight: .bold, design: .monospaced))
                                .foregroundColor(WatchPalette.steel)
                            Text(String(format: "%.1f°", motion.pitch))
                                .font(.system(size: 18, weight: .black, design: .rounded))
                                .monospacedDigit()
                                .foregroundColor(WatchPalette.amber)
                        }

                        VStack(spacing: 2) {
                            Text("ROLL")
                                .font(.system(size: 7, weight: .bold, design: .monospaced))
                                .foregroundColor(WatchPalette.steel)
                            Text(String(format: "%.1f°", motion.roll))
                                .font(.system(size: 18, weight: .black, design: .rounded))
                                .monospacedDigit()
                                .foregroundColor(WatchPalette.amber)
                        }
                    }

                    Rectangle()
                        .fill(WatchPalette.steel.opacity(0.3))
                        .frame(width: 80, height: 1)

                    HStack {
                        Circle()
                            .fill(abs(motion.pitch) < 3 && abs(motion.roll) < 3 ? WatchPalette.green : WatchPalette.red)
                            .frame(width: 8, height: 8)
                        Text(abs(motion.pitch) < 3 && abs(motion.roll) < 3 ? "STABLE" : "TILTED")
                            .font(.system(size: 9, weight: .black, design: .monospaced))
                            .foregroundColor(abs(motion.pitch) < 3 && abs(motion.roll) < 3 ? WatchPalette.green : WatchPalette.red)
                    }
                }
            }
            .frame(width: 142, height: 142)
        }
        .onAppear { motion.startUpdates() }
        .onDisappear { motion.stopUpdates() }
    }
}
