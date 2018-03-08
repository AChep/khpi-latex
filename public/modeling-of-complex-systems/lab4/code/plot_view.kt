class PlotView @JvmOverloads constructor(
        context: Context, attrs: AttributeSet? = null, defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    ...

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                touchDownX = event.x
                touchX = event.x
            }
            MotionEvent.ACTION_MOVE -> {
                if (isBeingDragged.not()) {
                    val ddx = abs(touchDownX - event.x)
                    if (ddx > touchSlop) {
                        isBeingDragged = true
                        parent.requestDisallowInterceptTouchEvent(true)
                    }
                }

                if (isBeingDragged) {
                    val dx = touchX - event.x

                    // Scale touch to plot
                    getDrawingRect(rect)
                    val ratioX = plot.window.size / rect.width()
                    val scaledDx = dx * ratioX

                    plot.window.start += scaledDx
                    updatePlotValues()
                    updatePlotPaths()
                    postInvalidateOnAnimation()
                }
                touchX = event.x
            }
            MotionEvent.ACTION_UP -> {
                isBeingDragged = false
            }
        }
        return true
    }

    ...

    private fun drawPlot(canvas: Canvas) {
        plot.functions.forEachIndexed { i, f ->
            val path = paths[i]
            val value = values[i]

            // Draw points
            paint.apply {
                strokeWidth = 8f
                color = f.style.color
                style = Paint.Style.FILL
            }

            val xf = plot.window.start + plot.window.size * VVV
            val yf = plot.max - f(xf)

            val ratioY = rect.height() / plot.height()
            val xv = rect.left + rect.width() * VVV
            val yv = rect.top + yf * ratioY
            canvas.drawCircle(xv, yv, 6 * density, paint)
            canvas.drawText(value, xv + 12 * density, yv + 4 * density, paint)

            // Draw function
            paint.apply {
                strokeWidth = 8f
                color = f.style.color
                style = Paint.Style.STROKE
            }

            canvas.drawPath(path, paint)
        }
    }

    ...

    private fun updatePlotPaths() {
        getDrawingRectWithPaddings(rect)

        val ratioX = rect.width() / plot.window.size
        val ratioY = rect.height() / plot.height()

        plot.functions.forEachIndexed { i, f ->
            val path = paths[i]
            path.reset()

            var first = true
            var x = plot.window.start
            val step = plot.window.size * STEP

            while (true) {
                // Draw a line plot of the
                // function
                val xl = x - plot.window.start
                val yl = plot.max - f(x)
                if (first) {
                    first = false
                    path.moveTo(
                            rect.left + xl * ratioX,
                            rect.top + yl * ratioY)
                } else {
                    path.lineTo(
                            rect.left + xl * ratioX,
                            rect.top + yl * ratioY)
                }

                if (x > plot.window.start + plot.window.size) {
                    break
                }

                x += step
            }
        }
    }
}