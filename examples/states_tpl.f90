module utils

use types
implicit none
private
public get_atomic_states_nonrel

contains

subroutine get_atomic_states_nonrel(Z, no, lo, fo)
! Returns all electron states of the form (n, l, f) for a given Z
integer, intent(in) :: Z ! atomic number
integer, intent(out), allocatable :: no(:), lo(:) ! quantum numbers "n" and "l"
real(dp), intent(out), allocatable :: fo(:) ! occupancy of the (n, l) state
! Note: sum(fo) == Z

integer :: n

select case (Z)
{% for s in states %}
    case ({{ s.Z }})
        n = {{ s.len_n }}
        allocate(no(n), lo(n), fo(n))
        no = (/ {% for x in s.n %}{{ x }}, {% endfor %}/)
        lo = (/ {% for x in s.l %}{{ x }}, {% endfor %}/)
        fo = (/ {% for x in s.f %}{{ x }}, {% endfor %}/)
{% endfor %}
    case default
        call stop_error("Z = " // str(Z) // " not supported.")
end select
end subroutine

end module