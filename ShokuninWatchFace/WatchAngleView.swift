import SwiftUI

struct WatchAngleView: View {
    @StateObject private var motion = MotionManager()

    var body: some View {
        VStack(spacing: 8) {
            Text("角度計")
                .font(.system(size: 16, weight: .black, design: .rounded))
                .foregroundStyle(WatchPalette.title)

            ZStack {
                Circle()
                    .fill(Color.black.opacity(0.44))
                    .overlay(Circle().stroke(WatchPalette.amber.opacity(0.45), lineWidth: 5))

                ForEach(0..<36, id: \.self) { index in
                    Rectangle()
                        .fill(index % 9 == 0 ? WatchPalette.amber : WatchPalette.steel.opacity(0.42))
                        .frame(width: index % 9 == 0 ? 2 : 1, height: index % 9 == 0 ? 12 : 6)
                        .offset(y: -58)
                        .rotationEffect(.degrees(Double(index) * 10))
                }

                Capsule()
                    .fill(WatchPalette.amber)
                    .frame(width: 5, height: 48)
                    .offset(y: -24)
                    .rotationEffect(.degrees(motion.angle))

                Circle()
                    .fill(WatchPalette.amber)
                    .frame(width: 18, height: 18)

                VStack(spacing: 0) {
                    Text(String(format: "%.1f°", motion.angle))
                        .font(.system(size: 26, weight: .black, design: .rounded))
                        .monospacedDigit()
                        .foregroundColor(WatchPalette.paper)
                    Text("ANGLE")
                        .font(.system(size: 8, weight: .black, design: .monospaced))
                        .foregroundColor(WatchPalette.amber)
                }
                .offset(y: 38)
            }
            .frame(width: 142, height: 142)
        }
        .onAppear { motion.startUpdates() }
        .onDisappear { motion.stopUpdates() }
    }
}
